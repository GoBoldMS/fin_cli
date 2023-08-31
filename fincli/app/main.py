import datetime
import logging
import os
import pandas as pd
from app.configurator import build_config
from cli.cli_stock_screener import select_filters_and_values
from stock_screening.content.stock_table import StockTableScreeningContent
from utils.web_scraper import fetch_page_sync
from logs.logger import logger
from stock_screening.locators.stock_table_locators import StockTableLocators


def fetch_urls(quarry, page_count):
    urls = [f"{quarry}&r={abs(20*(i) + 1)}" for i in range(page_count + 1)]
    return [fetch_page_sync(url) for url in urls]


def aggregate_rows(pages):
    rows = []
    for page_content in pages:
        tab = StockTableScreeningContent(page_content)
        rows.extend(tab.all_table_content)
    return [row.table_data for row in rows]


def build_dataframe(data_rows):
    df = pd.concat([pd.DataFrame(row) for row in data_rows])
    df.columns = StockTableLocators.PD_TABLE_COLUMNS
    df['Ticker'] = '=HYPERLINK("' + df['Link'] + '", "' + df['Ticker'] + '")'
    df.drop(columns=['Link'], axis=1, inplace=True)
    return df


def run_stock_screener(history: bool = False, debug: bool = False):
    logger.set_level(logging.DEBUG if debug else logging.INFO)

    config = build_config(use_history=history)
    logger.debug(f"Config: {config}", "Config created successfully:")

    quarry = select_filters_and_values(config)
    logger.debug(f"Quarry: {quarry}", 'Quarry created successfully:')

    logger.info(
        f"Fetching HTML content from {quarry}", 'Fetching HTML - Started')
    html_content = fetch_page_sync(quarry)
    logger.info(
        f"HTML content fetched from {quarry} successfully", "Fetching HTML - Completed")

    stock_screener_page = StockTableScreeningContent(html_content)

    pages = fetch_urls(quarry, stock_screener_page.page_count)
    data_rows = aggregate_rows(pages)

    if len(data_rows) == 0:
        logger.error("Data Handling --->",f"No data was found for the given filters"
                     )
        return

    final_df = build_dataframe(data_rows)

    logger.info(f"Data frame created successfully", "Data Handling --->")
    date = datetime.datetime.now().strftime('%Y-%m-%d_%H-%M')
    logger.info(f"Saving data frame to csv file", "Data Handling --->")
    file_path = os.path.join(
        os.getcwd(), f'workspace_output\stock_screener_{date}.csv')
    final_df.to_csv(file_path, index=False)
    logger.info(f"File saved to {file_path}", "Data Handling --->")
