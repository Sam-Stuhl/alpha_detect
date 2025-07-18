import yfinance as yf
import pandas as pd
from datetime import datetime

class Strategy:
    def __init__(self, type: str, ticker: str, capital: float = 1000.0):    
        self.type = type
        self.ticker = ticker
        self.capital = capital
        self.ticker_price_data_df = self.clean_df(yf.Ticker(ticker).history(start="2020-01-01", end=datetime.today().strftime('%Y-%m-%d')))
        
        
    def clean_df(self, df: pd.DataFrame):
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