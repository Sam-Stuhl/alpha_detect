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
    # AMD
    rsi_ticker = 'AMD'
    rsi_buy = 30
    rsi_sell = 70
    
    # #Nvidia
    # rsi_ticker = 'NVDA'
    # rsi_buy = 35
    # rsi_sell = 65
    
    # #Tesla
    # rsi_ticker = 'TSLA'
    # rsi_buy = 28
    # rsi_sell = 72
    
   # PriceThreshold(ticker, buy_price=buy, sell_price=sell, capital=1000, time_period='5Y')    
    RSIThreshold(rsi_ticker, buy_threshold=rsi_buy, sell_threshold=rsi_sell, capital=1000, time_period='1Y')