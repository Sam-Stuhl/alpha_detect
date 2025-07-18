from strategies import PriceThreshold, RSIThreshold, SMACrossover


if __name__ == "__main__":
    # Test Stocks
    
    # # Palantir
    # ticker = 'PLTR'
    # buy = 20
    # sell = 25
    
    # # AMD
    # ticker = 'AMD'
    # buy = 110
    # sell = 145
    
    # Tesla
    ticker = 'TSL'
    buy = 15
    sell = 16
    
    PriceThreshold(ticker, buy_price=buy, sell_price=sell)    
    