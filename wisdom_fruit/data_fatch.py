import datetime
import pandas_datareader as pdr
from pandas import DataFrame


class DataInsights:
    
    def __init__(self,data_frame: DataFrame) -> None:
        self.data_frame = data_frame
        
    
    def __repr__(self) -> str:
        return f"Sort object "
    
    def filter(self,filter: str, value: str,equal: bool = True):
        end = datetime.datetime.now() 
        start = end - datetime.timedelta(days=5*365)
        
        df = pdr.get_data_yahoo('^GSPC', start, end)  
        df.to_csv('sp500_data_last_5_years.csv')