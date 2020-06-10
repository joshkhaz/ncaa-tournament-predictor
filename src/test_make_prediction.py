from src.make_prediction import make_prediction
# set up logging
import logging

logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.INFO)
logger = logging.getLogger(__file__)

def test_make_prediction_happy():
    """
    Function to test make_prediction function used by the app. This is the happy path so make_prediction should return something.
    """
    logger.debug("Testing happy path for make prediction.")
    team_in_database = "Illinois"

    try:
        make_prediction(team_in_database)
        logger.info("Test passed. Prediction made successfully.")
    except:
        logger.warning("Test failed. Prediction could not be made.")

def test_make_prediction_unhappy():
    """
    Second function to test make_prediction function used by the app. This is the unhappy path so make_prediction should not return anything.
    """
    logger.debug("Testing unhappy path for make prediction.")
    team_not_in_database = "Chicago Bulls"

    try:
        make_prediction(team_not_in_database)
        logger.warning("Test failed. Prediction was made with team not in database.")
    except:
        logger.info("Test passed. Prediction was not made with team not in database.")