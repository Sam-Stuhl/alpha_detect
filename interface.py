from strategies import PriceThreshold, RSIThreshold, SMACrossover
import yfinance as yf

class CLI:
    def __init__(self, strategy: str = None, ticker: str = None, capital: float = None, time_period: str = None):
        self.strategies: dict[str: function] = {
            'Price Threshold': PriceThreshold,
            'RSI Threshold': RSIThreshold,
            'SMA Crossover': SMACrossover
            }
        self.strategy = self.get_strategy() if not strategy else strategy
        self.ticker = self.get_ticker() if not ticker else ticker
        self.starting_capital = self.get_capital() if not capital else capital
        self.time_period = self.get_time_period() if not time_period else time_period
        
        # Initialize Strategy   
        self.strategies[self.strategy](self.ticker, self.starting_capital, self.time_period)
    
    def get_strategy(self) -> str:
        for i, strategy in enumerate(self.strategies.keys()):
            print(f'({i + 1}) {strategy}')
        
        return list(self.strategies.keys())[int(input('Choose a Strategy: ')) - 1]
    
    def get_ticker(self) -> str:
        while True:
            ticker_choice: str = input('\nEnter the stock symbol you would like to test on: ').upper()
            if self.is_valid_ticker(ticker_choice): 
                return ticker_choice
            else:
                print(f'{ticker_choice} is not a stock. Please Enter a valid stock name (make sure to use the correct stock symbol)\n')
    
    def get_capital(self) -> float:
        try:
            return float(input('\nEnter starting capital (enter for $1000): '))
        except Exception:
            return 1000
            
    
    def get_time_period(self) -> str: 
        time_periods = [
            '1D',
            '1W',
            '1M',
            '3M',
            '6M',
            '1Y',
            '3Y',
            '5Y',
        ]
        
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