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
        ticker_data = yf.download(self.ticker, period=time_period) # Download ticker data
        ticker_data.columns = ticker_data.columns.droplevel(1) # Remove unnecessary ticker column label
        ticker_data.reset_index(inplace=True) # Reset the index
        ticker_data.rename(columns={'Datetime': 'Date'}, inplace=True)
        
        return ticker_data
    
    def back_test(self):
        raise NotImplementedError("Subclasses must implement back_test()")
    
    def calc_sharpe_ratio(self, daily_returns: pd.Series, risk_free_rate: float = 0.0) -> float:
        if daily_returns.std() == 0 or daily_returns.isna().all():
            return 0.0
        
        excess_returns = daily_returns - (risk_free_rate / 252)
        
        sharpe_ratio = excess_returns.mean() / excess_returns.std()
        annualized_sharpe = sharpe_ratio * np.sqrt(252)
        
        return round(annualized_sharpe, 3)