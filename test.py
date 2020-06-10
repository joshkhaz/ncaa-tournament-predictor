from src.test_cross_validation import test_cross_validation
from src.test_modelling import test_feature_engineering, test_model
from src.test_make_prediction import test_make_prediction_happy, test_make_prediction_unhappy
import config.config as config

if __name__ == '__main__':

    if config.GET_PERFORMANCE == True:
        test_cross_validation()
    test_feature_engineering()
    test_model()
    test_make_prediction_happy()
    test_make_prediction_unhappy()
