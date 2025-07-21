import yfinance as yf
import pandas as pd
from datetime import datetime

class Strategy:
    def __init__(self, type: str, buy_sell_keyword: str, ticker: str, capital: float, time_period: str, buy_threshold: float = None, sell_threshold: float = None):    
        self.type = type
        self.buy_sell_keyword = buy_sell_keyword
        self.ticker = ticker
        self.capital = capital
        
        if not(buy_threshold and sell_threshold):
            self.buy_threshold, self.sell_threshold = self.get_buy_and_sell_thresholds()
        else:
            self.buy_threshold = buy_threshold
            self.sell_threshold = sell_threshold
            
        self.ticker_data_df = self.get_ticker_data(time_period)
        
        
    
    def get_buy_and_sell_thresholds(self) -> tuple[float, float]:
        
        while True:
            buy_threshold = float(input(f'\nEnter the {self.buy_sell_keyword} to buy {self.ticker} at: '))
            sell_threshold = float(input(f'Enter the {self.buy_sell_keyword} to sell {self.ticker} at: '))
            
            if self.type == 'Price Threshold' and buy_threshold > self.capital:
                print(f"The buy {self.buy_sell_keyword} cannot be greater than the starting capital. Either enter a lower buy price or restart.")
            elif buy_threshold > sell_threshold:
                print(f"The buy {self.buy_sell_keyword} cannot be greater than the sell {self.buy_sell_keyword}. Try again.")
            else:
                break
        
        return (buy_threshold, sell_threshold)
    
    def get_ticker_data(self, time_period) -> pd.DataFrame:
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
        #return yf.Ticker(self.ticker).history(start=start, end=end)
        

    
    
    def clean_df(self, df: pd.DataFrame) -> pd.DataFrame:
        df.reset_index(inplace=True) # Add numerical index to the df
        # if self.type == 'Price Threshold':
        #     df = df[['Date', 'Close']]
        # elif self.type == 'RSI Threshold':
        #     pass
        # elif self.type == 'SMA Crossover':
        #     pass
        # else:
        #     print(f'Invalid strategy type declaration. {self.type} is not an acceptable strategy.')
        return df
    
    def back_test(self):
        raise NotImplementedError("Subclasses must implement back_test()")