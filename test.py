from strategies import PriceThreshold, RSIThreshold, SMACrossover


if __name__ == "__main__":
    """
    Price Threshold Test
    """
    
    # Palantir
    # ticker = 'PLTR'
    # buy = 20
    # sell = 25
    
    # AMD
    ticker = 'AMD'
    buy = 110
    sell = 145
    
    """
    RSI Threshold Test
    """
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
    
    """
    SMA Crossover Test
    """
    
    # # AMD
    # sma_ticker = 'AMD'
    # sma_short = 10
    # sma_long = 50
    
    # #Nvidia
    # sma_ticker = 'NVDA'
    # sma_short = 10
    # sma_long = 50
    
    # Apple
    sma_ticker = 'AAPL'
    sma_short = 10
    sma_long = 50
    
    #PriceThreshold(ticker, buy_price=buy, sell_price=sell, capital=1000, time_period='5Y')    
    #RSIThreshold(rsi_ticker, buy_threshold=rsi_buy, sell_threshold=rsi_sell, capital=1000, time_period='5Y')
    SMACrossover(sma_ticker, 1000, '5Y', sma_short, sma_long)