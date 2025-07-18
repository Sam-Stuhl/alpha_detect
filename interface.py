from strategies import PriceThreshold, RSIThreshold, SMACrossover
import yfinance as yf

def interface():
    strategies: dict[str: function] = {
        'Price Threshold': PriceThreshold,
        'RSI Threshold': RSIThreshold,
        'SMA Crossover': SMACrossover
        }
    
    for i, strategy in enumerate(strategies.keys()):
        print(f'({i + 1}) {strategy}')
    
    strategy_choice: str = list(strategies.keys())[int(input('Choose a Strategy: ')) - 1]
    
    
    while True:
        ticker_choice: str = input('\nEnter the stock name you would like to test on: ').upper()
        if is_valid_ticker(ticker_choice): 
            break 
        else:
            print(f'{ticker_choice} is not a stock. Please Enter a valid stock name (make sure to use the correct stock symbol)\n')
    
    
    try:
        starting_capital = float(input('\nEnter starting capital (enter for $1000): '))
        
        strategies[strategy_choice](ticker_choice, starting_capital)
    except Exception:
        strategies[strategy_choice](ticker_choice)
        
    
def is_valid_ticker(ticker: str) -> bool:
    try:
        stock = yf.Ticker(ticker)
        hist = stock.history(period='1d')
        return not hist.empty # If it is empty then, then it's not a valid ticker
    except Exception:
        return False