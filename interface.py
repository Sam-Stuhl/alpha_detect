from strategies import PriceThreshold, RSIThreshold, SMACrossover
import yfinance as yf

def interface():
    # Get Strategy
    strategies: dict[str: function] = {
        'Price Threshold': PriceThreshold,
        'RSI Threshold': RSIThreshold,
        'SMA Crossover': SMACrossover
        }
    
    for i, strategy in enumerate(strategies.keys()):
        print(f'({i + 1}) {strategy}')
    
    strategy_choice: str = list(strategies.keys())[int(input('Choose a Strategy: ')) - 1]
    
    # Get Stock Symbol
    while True:
        ticker_choice: str = input('\nEnter the stock symbol you would like to test on: ').upper()
        if is_valid_ticker(ticker_choice): 
            break 
        else:
            print(f'{ticker_choice} is not a stock. Please Enter a valid stock name (make sure to use the correct stock symbol)\n')
    
    # Get Starting Capital
    try:
        starting_capital = float(input('\nEnter starting capital (enter for $1000): '))
    except Exception:
        starting_capital = 1000
        
    print()
    
    # Get Time Period    
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
        
    time_period = time_periods[int(input('Choose a time period to backtest: ')) - 1]
     
    # Initialize Strategy   
    strategies[strategy_choice](ticker_choice, starting_capital, time_period)
    
def is_valid_ticker(ticker: str) -> bool:
    try:
        stock = yf.Ticker(ticker)
        hist = stock.history(period='1d')
        return not hist.empty # If it is empty then, then it's not a valid ticker
    except Exception:
        return False