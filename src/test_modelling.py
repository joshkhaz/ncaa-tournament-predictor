from src.modelling import feature_engineering, model
# set up logging
import logging

logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.INFO)
logger = logging.getLogger(__file__)

def test_feature_engineering():
    """
    Function to test feature_engineering step in model pipeline.
    """
    logger.debug("Attempting feature engineering.")
    try:
        feature_engineering()
        logger.info("Test passed. Feature engineering successful.")
    except:
        logger.warning("Test failed. Feature engineering could not be conducted.")

def test_model():
    """
    Function to test model step in model pipeline.
    """
    logger.debug("Attempting modelling.")
    try:
        model()
        logger.info("Test passed. Modelling successful.")
    except:
        logger.warning("Test failed. Modelling could not be conducted.")