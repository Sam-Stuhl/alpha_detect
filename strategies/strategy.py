import yfinance as yf
import pandas as pd
from datetime import datetime

class Strategy:
    def __init__(self, type: str, ticker: str, capital: float, time_period: str):    
        self.type = type
        self.ticker = ticker
        self.capital = capital
        self.ticker_price_data_df = self.get_ticker_price_data(time_period)
        
    
    def get_ticker_price_data(self, time_period) -> pd.DataFrame:
        # Set start and end times
        from dateutil.relativedelta import relativedelta
        
        end = datetime.today()
        
        if time_period == '1D':
            start = end - relativedelta(days=1)
        elif time_period == '1W':
            start = end - relativedelta(days=7)
        elif time_period == '1M':
            start = end - relativedelta(months=1)
        elif time_period == '3M':
            start = end - relativedelta(months=3)
        elif time_period == '6M':
            start = end - relativedelta(months=6)
        elif time_period == '1Y':
            start = end - relativedelta(years=1)
        elif time_period == '3Y':
            start = end - relativedelta(years=3)
        elif time_period == '5Y':
            start = end - relativedelta(years=5)
        else:
            start = '2020-01-01'
        
        return self.clean_df(yf.Ticker(self.ticker).history(start=start, end=end))
        

    
    
    def clean_df(self, df: pd.DataFrame) -> pd.DataFrame:
        df.reset_index(inplace=True) # Add numerical index to the df
        if self.type == 'Price Threshold':
            df = df[['Date', 'Close']]
        elif self.type == 'RSI Threshold':
            pass
        elif self.type == 'SMA Crossover':
            pass
        else:
            print(f'Invalid strategy type declaration. {self.type} is not an acceptable strategy.')
        return df
    
    def back_test(self):
        print(f"No back test function for {self.type} has been created yet.")