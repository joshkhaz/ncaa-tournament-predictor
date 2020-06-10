import sqlalchemy
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Float
from sqlalchemy.orm import sessionmaker
import config.config as config
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

engine = sqlalchemy.create_engine(config.DB_ENGINE_STRING)

Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()

def make_prediction(team):
    query = session.query(Preds.pred_round).filter(Preds.Team == team)
    prediction = query.first()[0]

    return prediction

