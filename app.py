import traceback
from flask import render_template, request, redirect, url_for
import logging.config
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from src.make_prediction import make_prediction
import pandas as pd

# Initialize the Flask application
app = Flask(__name__, template_folder="app/templates")

# Configure flask app from flask_config.py
app.config.from_pyfile('app/config/flaskconfig.py')

# Define LOGGING_CONFIG in flask_config.py - path to config file for setting
# up the logger (e.g. config/logging/local.conf)
logging.config.fileConfig(app.config["LOGGING_CONFIG"])
logger = logging.getLogger(app.config["APP_NAME"])
logger.debug('Test log')

# Initialize the database
db = SQLAlchemy(app)


@app.route('/')
def index():
    """Main view that lists songs in the database.
    Create view into index page that uses data queried from Track database and
    inserts it into the msiapp/templates/index.html template.
    Returns: rendered html template
    """

    try:
        try:
            predictions = list(pd.read_csv('./app/one_prediction.csv')['one_prediction'])
        except:
            predictions = []
        empty_preds = pd.DataFrame([' '], columns=['one_prediction'])
        empty_preds.to_csv("./app/one_prediction.csv")
        if len(predictions)==1:
            return render_template('index.html', predictions=predictions)
        elif len(predictions)==0:
            return render_template('index.html')

    except:
        traceback.print_exc()
        logger.warning("Not able to display tracks, error page returned")
        return render_template('error.html')


@app.route('/add', methods=['POST'])
def add_entry():
    """View that process a POST with new song input
    :return: redirect to index page
    """

    #try:
    team = request.form['team']
    try:
        round = make_prediction(team)
    except:
        round = "Team name is invalid. Please try again."
    one_prediction = pd.DataFrame([round], columns=['one_prediction'])
    one_prediction.to_csv("./app/one_prediction.csv")
    #logger.info("New song added: %s by %s", request.form['title'], request.form['artist'])
    return redirect(url_for('index'))
    #except:
    #    logger.warning("Not able to display tracks, error page returned")
    #    return render_template('error.html')


if __name__ == '__main__':
    app.run(debug=app.config["DEBUG"], port=app.config["PORT"], host=app.config["HOST"])