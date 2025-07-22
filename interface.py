from strategies import strategies

import yfinance as yf

class CLI:
    def __init__(self, ticker: str = None, capital: float = None, time_period: str = None):
        self.strategy_index = self.get_strategy()
        self.ticker = self.get_ticker() if not ticker else ticker
        self.starting_capital = self.get_capital() if not capital else capital
        self.time_period = self.get_time_period() if not time_period else time_period
        
        # Initialize Strategy   
        strategies[self.strategy_index](self.ticker, self.starting_capital, self.time_period)
    
    def get_strategy(self) -> int:
        for i, strategy in enumerate(strategies):
            print(f'({i + 1}) {strategy.name}')
        
        return int(input('Choose a Strategy: ')) - 1
    
    def get_ticker(self) -> str:
        while True:
            ticker_choice: str = input('\nEnter the stock symbol you would like to test on: ').upper()
            if self.is_valid_ticker(ticker_choice): 
                return ticker_choice
            else:
                print(f'{ticker_choice} is not a stock. Please Enter a valid stock name (make sure to use the correct stock symbol)\n')
    
    # Get the capital that the back tester will start with
    def get_capital(self) -> float:
        try:
            return float(input('\nEnter starting capital (enter for $1000): '))
        except Exception:
            return 1000
            
    # Get the time period that the back testing will take place in
    def get_time_period(self) -> str: 
        time_periods = strategies[self.strategy_index].time_periods
        
        print()
        for i, period in enumerate(time_periods):
            print(f'({i+1}) {period}')
            
        return time_periods[int(input('Choose a time period to backtest: ')) - 1]
     
    def is_valid_ticker(self, ticker: str) -> bool:
        try:
            stock = yf.Ticker(ticker)
            hist = stock.history(period='1d')
            return not hist.empty # If it is empty then, then it's not a valid ticker
        except Exception:
            return False