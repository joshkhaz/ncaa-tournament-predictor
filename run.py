import src.ingestion_and_schema_creation as ingest
import src.modelling as modelling
import config.config as config
from src.model_performance_metrics import cross_validation

if __name__ == '__main__':

    if config.INCLUDE_INGESTION == True:
        ingest.scrape_data(example_scrape=config.EXAMPLE_SCRAPE)
        ingest.raw_data_to_s3()
        ingest.write_schema_and_data_to_db()
    modelling.feature_engineering()
    if config.GET_PERFORMANCE == True:
        cross_validation()
    modelling.model()
    if config.INCLUDE_WRITING_PREDS_TO_DB == True:
        modelling.write_preds_to_db()

