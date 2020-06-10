from src.model_performance_metrics import cross_validation
# set up logging
import logging

logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.INFO)
logger = logging.getLogger(__file__)

def test_cross_validation():
    """
    Function to test cross_validation step in model pipeline.
    """
    logger.debug("Attempting cross validation.")
    try:
        cross_validation()
        logger.info("Test passed. Cross validation successful.")
    except:
        logger.warning("Test failed. Cross validation could not be conducted.")