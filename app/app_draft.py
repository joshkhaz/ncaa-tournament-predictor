import traceback
from flask import render_template, request, redirect, url_for
#import logging.config
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config.flaskconfig import SQLALCHEMY_DATABASE_URI
import sqlalchemy
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Float
from sqlalchemy.orm import sessionmaker

# Initialize the Flask application
app = Flask(__name__, template_folder="app/templates")

# Configure flask app from flask_config.py
app.config.from_pyfile('config/flaskconfig.py')

# Define LOGGING_CONFIG in flask_config.py - path to config file for setting
# up the logger (e.g. config/logging/local.conf)
#logging.config.fileConfig(app.config["LOGGING_CONFIG"])
#logger = logging.getLogger(app.config["APP_NAME"])
#logger.debug('Test log')

# Initialize the database
db = SQLAlchemy(app)

Base = declarative_base()

class Preds(Base):
    __tablename__ = 'preds'
    id = Column(Integer, primary_key=True, nullable=False)
    Team = Column(String(100), unique=False, nullable=False)
    pred_factor = Column(Integer, unique=False, nullable=False)
    pred_round = Column(String(100), unique=False, nullable=False)

engine = sqlalchemy.create_engine(SQLALCHEMY_DATABASE_URI)

Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()

def query_prediction(team):

    query = session.query(Preds.pred_round).filter(Preds.Team == team)
    prediction = q.first()[0]

    return prediction

@app.route('/')
def index():
    """Main view that lists songs in the database.
    Create view into index page that uses data queried from Track database and
    inserts it into the msiapp/templates/index.html template.
    Returns: rendered html template
    """

    try:
        preds = db.session.query(Preds).limit(app.config["MAX_ROWS_SHOW"]).all()
        #logger.debug("Index page accessed")
        return render_template('index.html', preds=preds)
    except:
        traceback.print_exc()
        #logger.warning("Not able to display predictions, error page returned")
        return render_template('error.html')


@app.route('/add', methods=['POST'])
def add_entry():
    """View that process a POST with new song input
    :return: redirect to index page
    """

    try:
        team1 = Preds(team=request.form['team'])
        return query_prediction(team), redirect(url_for('index'))
    except:
        #logger.warning("Not able to display tracks, error page returned")
        return render_template('error.html')


if __name__ == '__main__':
    app.run(debug=app.config["DEBUG"], port=app.config["PORT"], host=app.config["HOST"])