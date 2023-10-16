import yfinance as yf

from logger import logger


def calculate_price_to_data(financial_data, column_name):
    return financial_data[column_name]/financial_data['Shares Outstanding']


def ratio_between_two_values(value1, value2):
    return value1/value2


def adjust_assets(balance_sheet, asset_type, adjustment_factor, additional_subtracts):
    asset_value = balance_sheet.loc[asset_type].iloc[0] if asset_type in balance_sheet.index else 0
    for subtract in additional_subtracts:
        asset_value -= balance_sheet.loc[subtract].iloc[0] if subtract in balance_sheet.index else 0
    # Make the adjustment
    asset_value += (adjustment_factor *
                    balance_sheet.loc['Inventory'].iloc[0]) if 'Inventory' in balance_sheet.index else 0
    return asset_value


def get_financial_data(ticker_name):
    # Get the ticker object
    try:
        ticker = yf.Ticker(ticker_name)
    except:
        logger.error(f"Error getting ticker {ticker_name}")
        return None

    # Get the financial data
    balance_sheet = ticker.quarterly_balance_sheet
    info = ticker.info
    shares_outstanding = info['sharesOutstanding']
    market_cap = info['marketCap']
    total_assets = balance_sheet.loc['Total Assets'].iloc[0]
    total_equity = balance_sheet.loc['Stockholders Equity'].iloc[0]

    # Get the average price in the last 30 days
    history_30d = ticker.history(period="30d")
    average_price_30d = history_30d['Close'].quantile(0.5)

    # Adjust the current and total assets
    adjusted_current_assets = adjust_assets(
        balance_sheet, 'Current Assets', 0.3, ['Other Current Assets'])
    adjusted_total_assets = adjust_assets(balance_sheet, 'Total Assets', 0, [
                                          'Good Will', 'Other Assets'])

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
