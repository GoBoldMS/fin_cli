import pandas as pd

class Filters:

    def __init__(self, df: pd.DataFrame) -> None:
        self.df = df

    def filter_country(self, country: str):
        self.df = self.df[self.df["Country"] != country]
        return self

    def filter_countries(self, countries: list):
        self.df = self.df[~self.df["Country"].isin(countries)]
        return self

    def filter_sector(self, sector: str):
        self.df = self.df[self.df["Sector"] != sector]
        return self

    def filter_price(self, column, price: float, less_than: bool = True):
        if less_than:
            self.df = self.df[self.df[column] < price]
        else:
            self.df = self.df[self.df[column] > price]
        return self

    def get_data(self) -> pd.DataFrame:
        return self.df
