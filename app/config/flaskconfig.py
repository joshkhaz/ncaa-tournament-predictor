import os
DEBUG = True
LOGGING_CONFIG = "config/logging/local.conf"
PORT = 5000 #3306
APP_NAME = "msia423_ncaa_tournament"
SQLALCHEMY_TRACK_MODIFICATIONS = True
HOST = "0.0.0.0"
SQLALCHEMY_ECHO = False  # If true, SQL for queries made will be printed
MAX_ROWS_SHOW = 100

# Connection string
MYSQL_USER = '<insert credentials here>'
MYSQL_PASSWORD = '<insert credentials here>'
MYSQL_HOST = '<insert credentials here>'
MYSQL_PORT = '<insert credentials here>'
MYSQL_DATABASE = '<insert credentials here>'
MYSQL_CONNECTION = 'mysql+pymysql'
SQLALCHEMY_DATABASE_URI = "{}://{}:{}@{}:{}/{}".format(MYSQL_CONNECTION, MYSQL_USER, MYSQL_PASSWORD, MYSQL_HOST, MYSQL_PORT, MYSQL_DATABASE)



'''SQLALCHEMY_DATABASE_URI = os.environ.get('SQLALCHEMY_DATABASE_URI')
if SQLALCHEMY_DATABASE_URI is not None:
    pass
elif DB_HOST is None:
    SQLALCHEMY_DATABASE_URI = 'sqlite:///data/tracks.db'
else:
    SQLALCHEMY_DATABASE_URI = '{dialect}://{user}:{pw}@{host}:{port}/{db}'.format(dialect=DB_DIALECT, user=DB_USER,
                                                                                  pw=DB_PW, host=DB_HOST, port=DB_PORT,
                                                                                  db=DATABASE)'''
