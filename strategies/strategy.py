import yfinance as yf
import pandas as pd
import numpy as np
from datetime import datetime

class Strategy:
    def __init__(self, type: str, ticker: str, capital: float, time_period: str):    
        self.type = type
        self.ticker = ticker
        self.capital = capital
            
        self.ticker_data_df = self.get_ticker_data(time_period)
    
    def get_ticker_data(self, time_period) -> pd.DataFrame:
        # Set start and end times
        from dateutil.relativedelta import relativedelta
        
        end = datetime.today()
        
        if time_period == '1W':
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
            start = datetime.strptime('2020-01-01', '%Y-%m-%d')
        
        start = start.date()
        end = end.date()
        
        return yf.Ticker(self.ticker).history(start=start, end=end).reset_index()
    
    def back_test(self):
        raise NotImplementedError("Subclasses must implement back_test()")
    
    def calc_sharpe_ratio(self, daily_returns: pd.Series, risk_free_rate: float = 0.0) -> float:
        if daily_returns.std() == 0 or daily_returns.isna().all():
            return 0.0
        
        excess_returns = daily_returns - (risk_free_rate / 252)
        
        sharpe_ratio = excess_returns.mean() / excess_returns.std()
        annualized_sharpe = sharpe_ratio * np.sqrt(252)
        
        return round(annualized_sharpe, 3)