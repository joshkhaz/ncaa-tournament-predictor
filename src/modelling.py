import boto3
import pandas as pd
import pickle
import numpy as np
import config.config as config
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import GradientBoostingClassifier
from config.config import DB_ENGINE_STRING
import sqlalchemy
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Float
from sqlalchemy.orm import sessionmaker
# set up logging
import logging

logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.INFO)
logger = logging.getLogger(__file__)

Base = declarative_base()

class Preds(Base):
    """
    Create a data model for the database which will contain the 2020 predictions.
    """

    __tablename__ = 'preds'

    id = Column(Integer, primary_key=True, nullable=False)
    Team = Column(String(100), unique=False, nullable=False)
    pred_factor = Column(Integer, unique=False, nullable=False)
    pred_round = Column(String(100), unique=False, nullable=False)

    def __repr__(self):
        return '<Preds %r>' % self.Team

def feature_engineering():

    s3 = boto3.resource('s3', aws_access_key_id=config.AWS_ACCESS_KEY_ID, aws_secret_access_key=config.AWS_SECRET_ACCESS_KEY)

    s3.Bucket(config.S3_BUCKET).download_file(config.S3_BUCKET_DATA_FILENAME, config.LOCAL_S3_DATA_FILEPATH)

    cbb = pd.read_csv(config.LOCAL_S3_DATA_FILEPATH)

    avg_year_conf_power_rating = cbb.groupby(['Year','Conf']).mean()['Power_Rating'].to_frame()

    cbb['avg_conf_power_rating'] = cbb.apply(
        lambda x: avg_year_conf_power_rating.loc[x['Year']].loc[x['Conf']]['Power_Rating'] if x['Conf'] != 'ind' else .5,
        axis=1)

    cbb['Postseason'] = cbb['Postseason'].apply(lambda x: 'DIDNT_MAKE' if x == 'R68' else x)

    cbb['win_perc'] = cbb.Wins / cbb.Games

    cbb['wab_perc'] = cbb.WAB / cbb.Games

    cbb.to_csv(config.LOCAL_FE_DATA_FILEPATH)

def model():

    cbb = pd.read_csv(config.LOCAL_FE_DATA_FILEPATH)

    train = cbb[cbb.Year != 2020]
    test = cbb[cbb.Year == 2020]

    factor = pd.factorize(
        ['DIDNT_MAKE', 'R64', 'R32', 'Sweet Sixteen', 'Elite Eight', 'Final Four', 'Finals', 'CHAMPS'])
    factor_dict = {list(factor[1])[i]: list(factor[0])[i] for i in range(len(factor[1]))}
    train['postseason_factor'] = train['Postseason'].map(factor_dict)

    X_train = train[['ADJOE', 'ADJDE', 'EFG_O', 'EFG_D', 'TOR', 'TORD', 'ORB', 'DRB', 'FTR', 'FTRD',
                                         'Two_PO', 'Two_PD', 'Three_PO', 'Three_PD', 'ADJ_T', 'win_perc', 'wab_perc']]

    y_train = train['postseason_factor']

    X_test = test[['ADJOE', 'ADJDE', 'EFG_O', 'EFG_D', 'TOR', 'TORD', 'ORB', 'DRB', 'FTR', 'FTRD',
                   'Two_PO', 'Two_PD', 'Three_PO', 'Three_PD', 'ADJ_T', 'win_perc', 'wab_perc']]

    scaler = StandardScaler()
    X_train = scaler.fit_transform(X_train)
    X_test = scaler.transform(X_test)

    classifier = GradientBoostingClassifier(learning_rate=config.LEARNING_RATE,n_estimators =config.N_ESTIMATORS, min_samples_leaf=config.MIN_SAMPLES_LEAF, max_depth=config.MAX_DEPTH, random_state = config.RANDOM_STATE)
    classifier.fit(X_train, y_train)

    pickle.dump(classifier, open(config.MODEL_OBJECT_FILEPATH, 'wb'))

    test_preds = classifier.predict(X_test)

    test['pred_factor'] = test_preds

    preds = test[['Team', 'pred_factor']]

    round_dict = {0: 'Sorry, your team did not qualify for the tournament. Better luck next year!', 1: 'Congrats! Your team made it to the Round of 64!',
                  2: 'Wow! Your team made it to the Round of 32!', 3: 'Sensational! Your team made it to the Sweet Sixteen!',
                  4: 'Amazing! Your team made it to the Elite Eight!', 5: 'Unbelievable! Your team made it to the Final Four!',
                  6: 'Holy cow! Your team made it to the Finals!', 7: 'YOUR TEAM WAS CROWNED CHAMPIONS!!!'}

    preds['pred_round'] = preds['pred_factor'].map(round_dict)

    preds.reset_index(inplace=True)

    preds.to_csv(config.LOCAL_PREDS_DATA_FILEPATH)

def write_preds_to_db(local=False):

    """
    Create table schema and import predictions (from csv in repo, not S3 bucket) to RDS.
    """

    # Start SQLAlchemy session
    engine = sqlalchemy.create_engine(config.DB_ENGINE_STRING)
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    session = Session()

    # Delete contents from table if table already exists
    try:
        session.execute('''DELETE FROM preds''')
    except:
        pass

    # Import local csv contained scraped data
    preds = pd.read_csv(config.LOCAL_PREDS_DATA_FILEPATH)
    preds_rows = []

    # Collect data to write to database
    logger.info("Collecting data to write to database.")
    for index, row in preds.iterrows():
        preds_row = Preds(id=index,
                          Team=row.Team,
                          pred_factor=row.pred_factor,
                          pred_round=row.pred_round)
        preds_rows.append(preds_row)

    # Add all rows of data to table
    logger.info("Writing schema and data to database.")

    session.add_all(preds_rows)
    session.commit()
