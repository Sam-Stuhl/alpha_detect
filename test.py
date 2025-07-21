from strategies import PriceThreshold, RSIThreshold, SMACrossover


if __name__ == "__main__":
    # Test Stocks
    
    # # Palantir
    # ticker = 'PLTR'
    # buy = 20
    # sell = 25
    
    # AMD
    ticker = 'AMD'
    buy = 110
    sell = 145
    
    # RSI Test
    # # AMD
    # ticker = 'AMD'
    # buy = 30
    # sell = 70
    
    # #Nvidia
    # ticker = 'NVDA'
    # buy = 35
    # sell = 65
    
    # #Tesla
    # ticker = 'TSLA'
    # buy = 28
    # sell = 72
    
    PriceThreshold(ticker, buy_price=buy, sell_price=sell, capital=1000, time_period='5Y')    
    #RSIThreshold(ticker, capital=1000, time_period='5Y')