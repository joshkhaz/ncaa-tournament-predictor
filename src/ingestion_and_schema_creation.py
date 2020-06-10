# import environment variables and modules for scraping
import requests
from bs4 import BeautifulSoup
import pandas as pd
from config.config import BASE_URL_pt1, BASE_URL_pt2, LOCAL_RAW_DATA_FILEPATH
# import environment variables and modules for writing data to S3
from config.config import AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, S3_BUCKET, S3_BUCKET_DATA_FILENAME
import boto3
# import environment variables and modules for writing schema and data to RDS
from config.config import DB_ENGINE_STRING
import sqlalchemy
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Float
from sqlalchemy.orm import sessionmaker
# set up logging
import logging

logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.INFO)
logger = logging.getLogger(__file__)

def scrape_data(example_scrape=False):
    """
    Scrape statistics of all teams across all years since 2008 from the website.
    """

    # Create dataframe with required columns
    df = pd.DataFrame(columns=['Team', 'Conf', 'Games', 'Wins', 'ADJOE', 'ADJDE', 'Power_Rating', 'EFG_O', 'EFG_D',
                               'TOR', 'TORD', 'ORB', 'DRB', 'FTR', 'FTRD', 'Two_PO', 'Two_PD', 'Three_PO',
                               'Three_PD', 'ADJ_T', 'WAB', 'Postseason', 'Year'])

    # Scrape data from 2008 to 2019 inclusive
    if example_scrape==True:
        end_year=2010
    else:
        end_year=2020

    for year in range(2008,end_year):
        logger.info("Scraping data from "+str(year) + ".")

        # Set up ability to parse through website
        base_url = BASE_URL_pt1 + str(year) + BASE_URL_pt2
        r = requests.get(base_url)
        soup = BeautifulSoup(r.text, 'html.parser')

        if example_scrape==True:
            iterate_soup= 5
        else:
            iterate_soup= len(soup.find_all('tr'))

        # The website is arranged as a table where each row corresponds to a team and each column corresponds to a statistic. We are iterating through the rows.
        for i in range(iterate_soup):
            try:
                try:
                    # The top line will only work for teams that made it and have a value for "seed"
                    seed_index = soup.find_all('tr')[i].find_all('td')[1].text.split().index('seed,')

                    team = ' '.join(soup.find_all('tr')[i].find_all('td')[1].text.split()[0:seed_index - 1])
                    conf = soup.find_all('tr')[i].find_all('td')[2].text
                    games = int(soup.find_all('tr')[i].find_all('td')[4].text.split('-')[0]) + int(
                        soup.find_all('tr')[i].find_all('td')[4].text.split('-')[1])
                    wins = int(soup.find_all('tr')[i].find_all('td')[4].text.split('-')[0])
                    adjoe = float(str(soup.find_all('tr')[i].find_all('td')[5]).split('>')[1].split('<')[0])
                    adjde = float(str(soup.find_all('tr')[i].find_all('td')[6]).split('>')[1].split('<')[0])
                    power_rating = float(str(soup.find_all('tr')[i].find_all('td')[7]).split('>')[1].split('<')[0])
                    efg_o = float(str(soup.find_all('tr')[i].find_all('td')[8]).split('>')[1].split('<')[0])
                    efg_d = float(str(soup.find_all('tr')[i].find_all('td')[9]).split('>')[1].split('<')[0])
                    tor = float(str(soup.find_all('tr')[i].find_all('td')[10]).split('>')[1].split('<')[0])
                    tord = float(str(soup.find_all('tr')[i].find_all('td')[11]).split('>')[1].split('<')[0])
                    orb = float(str(soup.find_all('tr')[i].find_all('td')[12]).split('>')[1].split('<')[0])
                    drb = float(str(soup.find_all('tr')[i].find_all('td')[13]).split('>')[1].split('<')[0])
                    ftr = float(str(soup.find_all('tr')[i].find_all('td')[14]).split('>')[1].split('<')[0])
                    ftrd = float(str(soup.find_all('tr')[i].find_all('td')[15]).split('>')[1].split('<')[0])
                    two_po = float(str(soup.find_all('tr')[i].find_all('td')[16]).split('>')[1].split('<')[0])
                    two_pd = float(str(soup.find_all('tr')[i].find_all('td')[17]).split('>')[1].split('<')[0])
                    three_po = float(str(soup.find_all('tr')[i].find_all('td')[18]).split('>')[1].split('<')[0])
                    three_pd = float(str(soup.find_all('tr')[i].find_all('td')[19]).split('>')[1].split('<')[0])
                    adj_t = float(str(soup.find_all('tr')[i].find_all('td')[20]).split('>')[1].split('<')[0])
                    wab = float(str(soup.find_all('tr')[i].find_all('td')[21]).split('>')[1].split('<')[0])
                    postseason = ' '.join(soup.find_all('tr')[i].find_all('td')[1].text.split()[seed_index + 1:])

                    stats = [team, conf, games, wins, adjoe, adjde, power_rating, efg_o, efg_d, tor, tord,
                             orb, drb, ftr, ftrd, two_po, two_pd, three_po, three_pd, adj_t, wab, postseason, year]
                    stats = pd.Series(stats, index=df.columns)

                    # Add row to dataframe
                    df = df.append(stats, ignore_index=True)

                except:
                    # Teams that didnt make the tournament have no index for seed
                    team = ' '.join(soup.find_all('tr')[i].find_all('td')[1].text.split())
                    conf = soup.find_all('tr')[i].find_all('td')[2].text
                    games = int(soup.find_all('tr')[i].find_all('td')[4].text.split('-')[0]) + int(
                        soup.find_all('tr')[i].find_all('td')[4].text.split('-')[1])
                    wins = int(soup.find_all('tr')[i].find_all('td')[4].text.split('-')[0])
                    adjoe = float(str(soup.find_all('tr')[i].find_all('td')[5]).split('>')[1].split('<')[0])
                    adjde = float(str(soup.find_all('tr')[i].find_all('td')[6]).split('>')[1].split('<')[0])
                    power_rating = float(str(soup.find_all('tr')[i].find_all('td')[7]).split('>')[1].split('<')[0])
                    efg_o = float(str(soup.find_all('tr')[i].find_all('td')[8]).split('>')[1].split('<')[0])
                    efg_d = float(str(soup.find_all('tr')[i].find_all('td')[9]).split('>')[1].split('<')[0])
                    tor = float(str(soup.find_all('tr')[i].find_all('td')[10]).split('>')[1].split('<')[0])
                    tord = float(str(soup.find_all('tr')[i].find_all('td')[11]).split('>')[1].split('<')[0])
                    orb = float(str(soup.find_all('tr')[i].find_all('td')[12]).split('>')[1].split('<')[0])
                    drb = float(str(soup.find_all('tr')[i].find_all('td')[13]).split('>')[1].split('<')[0])
                    ftr = float(str(soup.find_all('tr')[i].find_all('td')[14]).split('>')[1].split('<')[0])
                    ftrd = float(str(soup.find_all('tr')[i].find_all('td')[15]).split('>')[1].split('<')[0])
                    two_po = float(str(soup.find_all('tr')[i].find_all('td')[16]).split('>')[1].split('<')[0])
                    two_pd = float(str(soup.find_all('tr')[i].find_all('td')[17]).split('>')[1].split('<')[0])
                    three_po = float(str(soup.find_all('tr')[i].find_all('td')[18]).split('>')[1].split('<')[0])
                    three_pd = float(str(soup.find_all('tr')[i].find_all('td')[19]).split('>')[1].split('<')[0])
                    adj_t = float(str(soup.find_all('tr')[i].find_all('td')[20]).split('>')[1].split('<')[0])
                    wab = float(str(soup.find_all('tr')[i].find_all('td')[21]).split('>')[1].split('<')[0])
                    postseason = 'DIDNT_MAKE'

                    stats = [team, conf, games, wins, adjoe, adjde, power_rating, efg_o, efg_d, tor, tord,
                             orb, drb, ftr, ftrd, two_po, two_pd, three_po, three_pd, adj_t, wab, postseason, year]
                    stats = pd.Series(stats, index=df.columns)

                    # Add row to dataframe
                    df = df.append(stats, ignore_index=True)
            except:
                # The website contains some extra headers that dont correspond to teams and these are to be ignored
                pass

    # Scrape 2020 data
    year = 2020
    logger.info("Scraping data from " + str(year) + ".")

    # Set up ability to parse through website
    base_url = BASE_URL_pt1 + str(year) + BASE_URL_pt2
    r = requests.get(base_url)
    soup = BeautifulSoup(r.text, 'html.parser')

    # The website is arranged as a table where each row corresponds to a team and each column corresponds to a statistic. We are iterating through the rows.
    for i in range(iterate_soup):
        try:
            team = ' '.join(soup.find_all('tr')[i].find_all('td')[1].text.split())
            conf = soup.find_all('tr')[i].find_all('td')[2].text
            games = int(soup.find_all('tr')[i].find_all('td')[4].text.split('-')[0]) + int(
                soup.find_all('tr')[i].find_all('td')[4].text.split('-')[1])
            wins = int(soup.find_all('tr')[i].find_all('td')[4].text.split('-')[0])
            adjoe = float(str(soup.find_all('tr')[i].find_all('td')[5]).split('>')[1].split('<')[0])
            adjde = float(str(soup.find_all('tr')[i].find_all('td')[6]).split('>')[1].split('<')[0])
            power_rating = float(str(soup.find_all('tr')[i].find_all('td')[7]).split('>')[1].split('<')[0])
            efg_o = float(str(soup.find_all('tr')[i].find_all('td')[8]).split('>')[1].split('<')[0])
            efg_d = float(str(soup.find_all('tr')[i].find_all('td')[9]).split('>')[1].split('<')[0])
            tor = float(str(soup.find_all('tr')[i].find_all('td')[10]).split('>')[1].split('<')[0])
            tord = float(str(soup.find_all('tr')[i].find_all('td')[11]).split('>')[1].split('<')[0])
            orb = float(str(soup.find_all('tr')[i].find_all('td')[12]).split('>')[1].split('<')[0])
            drb = float(str(soup.find_all('tr')[i].find_all('td')[13]).split('>')[1].split('<')[0])
            ftr = float(str(soup.find_all('tr')[i].find_all('td')[14]).split('>')[1].split('<')[0])
            ftrd = float(str(soup.find_all('tr')[i].find_all('td')[15]).split('>')[1].split('<')[0])
            two_po = float(str(soup.find_all('tr')[i].find_all('td')[16]).split('>')[1].split('<')[0])
            two_pd = float(str(soup.find_all('tr')[i].find_all('td')[17]).split('>')[1].split('<')[0])
            three_po = float(str(soup.find_all('tr')[i].find_all('td')[18]).split('>')[1].split('<')[0])
            three_pd = float(str(soup.find_all('tr')[i].find_all('td')[19]).split('>')[1].split('<')[0])
            adj_t = float(str(soup.find_all('tr')[i].find_all('td')[20]).split('>')[1].split('<')[0])
            wab = float(str(soup.find_all('tr')[i].find_all('td')[21]).split('>')[1].split('<')[0])
            postseason = 'UNKNOWN'

            stats = [team, conf, games, wins, adjoe, adjde, power_rating, efg_o, efg_d, tor, tord,
                     orb, drb, ftr, ftrd, two_po, two_pd, three_po, three_pd, adj_t, wab, postseason, year]
            stats = pd.Series(stats, index=df.columns)

            # Add row to dataframe
            df = df.append(stats, ignore_index=True)
        except:
            # The website contains some extra headers that dont correspond to teams and these are to be ignored
            pass

    if example_scrape==True:
        filename_to_write = LOCAL_RAW_DATA_FILEPATH[:-4]+"_example.csv"
    else:
        filename_to_write = LOCAL_RAW_DATA_FILEPATH

    try:
        df.to_csv(filename_to_write, index=False)
        logger.info("Wrote scraped data to csv.")
    except:
        logger.error("Unable to write data to csv.")

def raw_data_to_s3():
    """
    Write scraped data to a bucket in S3.
    """

    logger.info("Writing raw data to S3.")

    try:
        s3 = boto3.client('s3', aws_access_key_id=AWS_ACCESS_KEY_ID, aws_secret_access_key=AWS_SECRET_ACCESS_KEY)
        logger.info("Established S3 client.")
    except:
        logger.error("Could not establish S3 client.")

    try:
        s3.upload_file(LOCAL_RAW_DATA_FILEPATH, S3_BUCKET, S3_BUCKET_DATA_FILENAME)
        logger.info("Uploaded file to S3.")
    except:
        logger.error("Could not upload file to S3.")


def write_schema_and_data_to_db(local=False):
    """
    Create table schema and import raw data (from csv in repo, not S3 bucket) to RDS.
    """

    Base = declarative_base()

    class Stats(Base):
        """
        Create a data model for the database which will contain team statistics.
        """

        __tablename__ = 'stats'

        id = Column(Integer, primary_key=True, nullable=False)
        Team = Column(String(100), unique=False, nullable=False)
        Conf = Column(String(100), unique=False, nullable=False)
        Games = Column(Integer, unique=False, nullable=False)
        Wins = Column(Integer, unique=False, nullable=False)
        ADJOE = Column(Float, unique=False, nullable=False)
        ADJDE = Column(Float, unique=False, nullable=False)
        Power_Rating = Column(Float, unique=False, nullable=False)
        EFG_O = Column(Float, unique=False, nullable=False)
        EFG_D = Column(Float, unique=False, nullable=False)
        TOR = Column(Float, unique=False, nullable=False)
        TORD = Column(Float, unique=False, nullable=False)
        ORB = Column(Float, unique=False, nullable=False)
        DRB = Column(Float, unique=False, nullable=False)
        FTR = Column(Float, unique=False, nullable=False)
        FTRD = Column(Float, unique=False, nullable=False)
        Two_PO = Column(Float, unique=False, nullable=False)
        Two_PD = Column(Float, unique=False, nullable=False)
        Three_PO = Column(Float, unique=False, nullable=False)
        Three_PD = Column(Float, unique=False, nullable=False)
        ADJ_T = Column(Float, unique=False, nullable=False)
        WAB = Column(Float, unique=False, nullable=False)
        Postseason = Column(String(100), unique=False, nullable=True)
        Year = Column(Integer, unique=False, nullable=False)

        def __repr__(self):
            return '<Stats %r>' % self.Team

    # Start SQLAlchemy session
    if local==False:
        engine = sqlalchemy.create_engine(DB_ENGINE_STRING)
    else:
        engine = sqlalchemy.create_engine(DB_ENGINE_STRING)
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    session=Session()

    # Delete contents from table if table already exists
    try:
        session.execute('''DELETE FROM stats''')
    except:
        pass

    # Import local csv contained scraped data
    cbb = pd.read_csv(LOCAL_RAW_DATA_FILEPATH)
    stats_rows = []

    # Collect data to write to database
    logger.info("Collecting data to write to database.")
    for index, row in cbb.iterrows():
        stats_row = Stats(id = index,
                          Team=row.Team,
                          Conf = row.Conf,
                          Games = row.Games,
                          Wins = row.Wins,
                          ADJOE = row.ADJOE,
                          ADJDE = row.ADJDE,
                          Power_Rating = row.Power_Rating,
                          EFG_O = row.EFG_O,
                          EFG_D = row.EFG_D,
                          TOR = row.TOR,
                          TORD = row.TORD,
                          ORB = row.ORB,
                          DRB = row.DRB,
                          FTR = row.FTR,
                          FTRD = row.FTRD,
                          Two_PO = row.Two_PO,
                          Two_PD = row.Two_PD,
                          Three_PO = row.Three_PO,
                          Three_PD = row.Three_PD,
                          ADJ_T = row.ADJ_T,
                          WAB = row.WAB,
                          Postseason = row.Postseason,
                          Year = row.Year)
        stats_rows.append(stats_row)

    # Add all rows of data to table
    logger.info("Writing schema and data to database.")
    try:
        session.add_all(stats_rows)
        session.commit()
        if local==False:
            logger.info("Stats table created and data written to RDS.")
        else:
            logger.info("Stats table created and data written to SQLite.")
    except:
        logger.error("Could not create stats table or write data to database.")