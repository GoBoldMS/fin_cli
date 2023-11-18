# import yfinance as yf
from math import nan
import re
import yahooquery as yq
from logger import logger


def calculate_price_to_data(financial_data, column_name):
    return financial_data[column_name]/financial_data['Shares Outstanding']


def ratio_between_two_values(value1, value2):
    if value2 == 0:
        return 0
    return value1/value2


def adjust_assets(balance_sheet, asset_type, adjustment_factor, additional_subtracts):
    try:
        asset_value = balance_sheet.iloc[-1][asset_type] if not int else balance_sheet.iloc[-2][asset_type]
    except KeyError:
        return None

    for subtract in additional_subtracts:
        try:
            sub = balance_sheet.iloc[-1][subtract] if not int else balance_sheet.iloc[-2][subtract]
        except KeyError:
            sub = None
        asset_value -= sub if not int else 0
    if adjustment_factor == 0:
        return asset_value
    # Make the adjustment
    try:
        inventory = balance_sheet.iloc[-1]['Inventory'] if not int else balance_sheet.iloc[-2]['Inventory']
    except KeyError:
        inventory = None
    asset_value += (adjustment_factor *
                    inventory) if not int else 0
    return asset_value


def get_financial_data(ticker_name: str):
    # Get the ticker object
    try:
        ticker = yq.Ticker(ticker_name)

    # Get the financial data
        balance_sheet = ticker.balance_sheet(frequency='q')
        if balance_sheet is None:
            logger.error(
                f"Error getting balance sheet for ticker {ticker_name}")
            return None
        if ticker.summary_detail is None:
            logger.error(
                f"Error getting summary_detail for ticker {ticker_name}")
            return None
        if ticker.key_stats is None:
            logger.error(f"Error getting key_stats for ticker {ticker_name}")
            return None
    except Exception as e:
        logger.error(f"Error getting ticker {ticker_name} - {e}")
        return None

    shares_outstanding = ticker.key_stats[ticker_name]['sharesOutstanding']
    market_cap = ticker.summary_detail[ticker_name]['marketCap']

    total_assets = balance_sheet.iloc[-1]['TotalAssets']
    total_equity = balance_sheet.iloc[-1]['StockholdersEquity']

    # Get the average price in the last 30 days
    history_30d = ticker.history(period="1mo")
    average_price_30d = history_30d['close'].quantile(0.5)

    # Adjust the current and total assets
    adjusted_current_assets = adjust_assets(
        balance_sheet, 'CurrentAssets', 0.3, ['OtherCurrentAssets'])
    adjusted_total_assets = adjust_assets(balance_sheet, 'TotalAssets', 0, [
                                          'Goodwill', 'OtherNonCurrentAssets'])

    return {
        'Symbol': ticker_name,
        'Market Cap': market_cap,
        'Shares Outstanding': shares_outstanding,
        'Total Assets': total_assets,
        'Adjusted Total Assets': adjusted_total_assets,
        'Adjusted Total Current Assets': adjusted_current_assets,
        'Total Equity': total_equity,
        'Average Price in Last 30 Days': average_price_30d,
    }
