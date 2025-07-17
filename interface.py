from strategies import PriceThreshold, RSIThreshold, SMACrossover

def interface():
    strategies: dict[str: function] = {
        'Price Threshold': PriceThreshold,
        'RSI Threshold': RSIThreshold,
        'SMA Crossover': SMACrossover
        }
    
    for i, strategy in enumerate(strategies.keys()):
        print(f'({i + 1}) {strategy}')
    
    choice: str = list(strategies.keys())[int(input('Choose a Strategy: ')) - 1]
    
    strategies[choice]()