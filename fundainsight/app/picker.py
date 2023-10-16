from pandas import DataFrame
import cProfile
from concurrent.futures import ThreadPoolExecutor
from ..calculators.equity_calc import get_financial_data,calculate_price_to_data, ratio_between_two_values
from logger import logger

def add_new_columns(df: DataFrame):
    df["price_by_assets"] = df.apply(lambda x: calculate_price_to_data(x,'Adjusted Total Assets'), axis=1)
    df["price_by_current_assets"] = df.apply(lambda x: calculate_price_to_data(x,'Adjusted Total Current Assets'), axis=1)
    df["price/price_to_current_assets_ratio"] = df.apply(lambda x: ratio_between_two_values(x["Average Price in Last 30 Days"], x["price_by_current_assets"]), axis=1)
    df["price/price_to_assets_ratio"] = df.apply(lambda x: ratio_between_two_values(x["Average Price in Last 30 Days"], x["price_by_assets"]), axis=1)
    return df


def picker(df: DataFrame|None):
    
    if df is None:
        return
    
    logger.info(f"Getting Financial Data --->")
    
 
    with ThreadPoolExecutor() as executor:
        results = list(executor.map(get_financial_data, df["Symbol"]))

        valid_results = [res for res in results if res is not None]
        df_fundamentals = DataFrame(valid_results)
    
    # df_fundamentals = DataFrame([get_financial_data(ticker) for ticker in df["Symbol"]]) #df[df.groupby('Ticker').apply(lambda x: get_financial_data(x['Ticker']))]
    df_fundamentals['Ticker'] = df['Ticker'].values
    df_fundamentals['Sector'] = df['Sector'].values
    logger.info(f"Calculating the price to assets ratio", "Calculating the price to assets ratio --->")

    df_fundamentals = add_new_columns(df_fundamentals)
        # Filter columns
    columns_to_retain = [
        'Ticker',
        'Sector',
        'Market Cap',
        'Average Price in Last 30 Days', 
        'price_by_assets', 
        'price_by_current_assets', 
        'price/price_to_current_assets_ratio', 
        'price/price_to_assets_ratio'
    ]
        
    df_fundamentals = df_fundamentals[columns_to_retain]

    return df_fundamentals



if __name__ == "__main__":
    # Sample DataFrame for testing
    df_sample = DataFrame({"Symbol": ["AAPL", "MSFT", "GOOGL"],"Ticker":["AAPL", "MSFT", "GOOGL"]})  # Add more tickers if needed
    
    profiler = cProfile.Profile()
    profiler.enable()
    
    picker(df_sample)
    
    profiler.disable()
    profiler.dump_stats("profile_results.pstat")
