import logging
from .configurator import build_config
from logger.logger import logger
from .picker import picker
from .fincli import get_recommended_stocks


def get_opportunities(history: bool = False, debug: bool = False, set_filters: str = ""):
    logger.set_level(logging.DEBUG if debug else logging.INFO)
    config = build_config(use_history=history, filters=set_filters)

    if (config.filters is None or config.filters == ()):
        logger.error("No filters were provided or could not be parsed.")
        return

    df_stocks = get_recommended_stocks(filters=config.filters)

    data = picker(df_stocks)
    
    if data is None:
        return
    logger.info("Saving results to csv..")
    data.to_csv(config.file_path("funda_insight_result")
)
    
    return data
