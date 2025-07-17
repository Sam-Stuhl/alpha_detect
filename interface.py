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
    
    print()
    
    while True:
        ticker_choice: str = input('Enter the stock name you would like to test on: ')
        if is_valid_ticker(ticker_choice): 
            break 
        else:
            print(f'{ticker_choice} is not a stock. Please Enter a valid stock name (make sure to use the correct stock symbol)\n')
    
    strategies[strategy_choice](ticker_choice)
    
def is_valid_ticker(ticker: str) -> bool:
    try:
        stock = yf.Ticker(ticker)
        hist = stock.history(period='1d')
        return not hist.empty # If it is empty then, then it's not a valid ticker
    except Exception:
        return False