import os

MYSQL_USER = os.environ.get('MYSQL_USER')
if MYSQL_USER is None:
    MYSQL_USER = 'msia423instructor'

MYSQL_PASSWORD = os.environ.get('MYSQL_PASSWORD')
if MYSQL_PASSWORD is None:
    MYSQL_PASSWORD = 'jjk555'

MYSQL_HOST = os.environ.get('MYSQL_HOST')
if MYSQL_HOST is None:
    MYSQL_HOST = 'msia423-josh-khazanov.c7n6qsjm5ezb.us-east-1.rds.amazonaws.com'

MYSQL_PORT = os.environ.get('MYSQL_PORT')
if MYSQL_PORT is None:
    MYSQL_PORT = 3306

MYSQL_DATABASE = os.environ.get('MYSQL_DATABASE')
if MYSQL_DATABASE is None:
    MYSQL_DATABASE = 'msia423_ncaa_tournament'

LOCAL_DB = os.environ.get('LOCAL_DB')
if LOCAL_DB is None:
    LOCAL_DB = False

MYSQL_CONNECTION = 'mysql+pymysql'

SQLITE_PATH = 'data/ncaa_tournament.db'

if LOCAL_DB==False:
    DB_ENGINE_STRING = "{}://{}:{}@{}:{}/{}".format(MYSQL_CONNECTION, MYSQL_USER, MYSQL_PASSWORD, MYSQL_HOST, MYSQL_PORT, MYSQL_DATABASE)
else:
    DB_ENGINE_STRING = "sqlite:////"+SQLITE_PATH

#Pipeline
INCLUDE_INGESTION = os.environ.get('INCLUDE_INGESTION')
if INCLUDE_INGESTION is None:
    INCLUDE_INGESTION = False

INCLUDE_WRITING_PREDS_TO_DB = os.environ.get('INCLUDE_WRITING_PREDS_TO_DB')
if INCLUDE_WRITING_PREDS_TO_DB is None:
    INCLUDE_WRITING_PREDS_TO_DB = False

GET_PERFORMANCE = os.environ.get('GET_PERFORMANCE')
if GET_PERFORMANCE is None:
    GET_PERFORMANCE = False

#S3 and AWS

S3_BUCKET = os.environ.get('S3_BUCKET')
if S3_BUCKET is None:
    S3_BUCKET = 'jjk555'

S3_BUCKET_DATA_FILENAME = "cbb.csv"

AWS_ACCESS_KEY_ID = os.environ.get('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = os.environ.get('AWS_SECRET_ACCESS_KEY')

# Web scraping env variables

EXAMPLE_SCRAPE = os.environ.get('EXAMPLE_SCRAPE')
if EXAMPLE_SCRAPE is None:
    EXAMPLE_SCRAPE = True

BASE_URL_pt1 = 'http://barttorvik.com/trank.php?year='
BASE_URL_pt2 = '&sort=&conlimit=#'
LOCAL_RAW_DATA_FILEPATH = "/data/cbb_local.csv"

#Modelling
LOCAL_S3_DATA_FILEPATH = "/data/cbb_s3.csv"
LOCAL_FE_DATA_FILEPATH = "/data/cbb_fe.csv"
MODEL_OBJECT_FILEPATH = '/data/trained_model_object.sav'
LOCAL_PREDS_DATA_FILEPATH = "/data/predictions.csv"
LEARNING_RATE = 0.1
N_ESTIMATORS = 100
MIN_SAMPLES_LEAF = 5
MAX_DEPTH = 3
RANDOM_STATE = 21

#Model Tuning
NUMBER_OF_CV_REPLICATES = 1
F1_SCORE_FILE_PATH = "/data/f1_score.csv"