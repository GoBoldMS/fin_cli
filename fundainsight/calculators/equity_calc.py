import yfinance as yf
# import yahooquery as yq
from logger import logger


def calculate_price_to_data(financial_data, column_name):
    return financial_data[column_name]/financial_data['Shares Outstanding']


def ratio_between_two_values(value1, value2):
    if value2 == 0:
        return 0
    return value1/value2


def adjust_assets(balance_sheet, asset_type, adjustment_factor, additional_subtracts):
    try:
        # asset_value = balance_sheet.iloc[-1][asset_type] if not int else balance_sheet.iloc[-2][asset_type]
        asset_value = balance_sheet.loc[asset_type].iloc[1] if asset_type in balance_sheet.index else 0
    except KeyError:
        return None

    for subtract in additional_subtracts:
        try:
            # asset_value  -= balance_sheet.loc[subtract].iloc[0] if subtract in balance_sheet.index else  0
            # if not int else balance_sheet.iloc[-2][subtract]
            sub = balance_sheet.loc[subtract].iloc[1]
        except KeyError:
            sub = None
        if sub is not None and sub > 0:
            asset_value -= sub
    if adjustment_factor == 0:
        return asset_value
    # Make the adjustment
    try:
        # inventory = balance_sheet.iloc[-1]['Inventory'] if not int else balance_sheet.iloc[-2]['Inventory']\
        inventory = balance_sheet['Inventory'].iloc[1]  # if not int else balance_sheet.iloc[-2]['Inventory']
    except KeyError:
        inventory = None
    asset_value += (adjustment_factor *
                    inventory) if not int else 0
    return asset_value


def get_financial_data(ticker_name: str):
    # Get the ticker object
    try:
        ticker = yf.Ticker(ticker_name)

    # Get the financial data
        balance_sheet = ticker.quarterly_balance_sheet
        if balance_sheet is None:
            logger.error(
                f"Error getting balance sheet for ticker {ticker_name}")
            return None
        if ticker.info is None:
            logger.error(
                f"Error getting summary_detail for ticker {ticker_name}")
            return None
        # if ticker.key_stats is None:
        #     logger.error(f"Error getting key_stats for ticker {ticker_name}")
        #     return None
    except Exception as e:
        logger.error(f"Error getting ticker {ticker_name} - {e}")
        return None
    shares_outstanding = ticker.info['sharesOutstanding']
    market_cap = ticker.info['marketCap']

    # shares_outstanding = ticker.info[ticker_name]['sharesOutstanding']
    # market_cap = ticker.info[ticker_name]['marketCap']

    # .iloc[1] will get you the last year / quarter
    total_assets = balance_sheet.loc['Total Assets'].iloc[1]
    total_equity = balance_sheet.loc['Stockholders Equity'].iloc[1]

    # Get the average price in the last 30 days
    history_30d = ticker.history()
    average_price_30d = history_30d['Close'].quantile(0.5)

    # Adjust the current and total assets
    adjusted_current_assets = adjust_assets(
        balance_sheet,  'Current Assets', 0.3, ['Other Current Assets'])
    adjusted_total_assets = adjust_assets(balance_sheet, "Total Assets", 0, [
        "Goodwill",  'Other Non Current Assets'])

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
