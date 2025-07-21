from .price_threshold import PriceThreshold
from .rsi_threshold import RSIThreshold
from .sma_crossover import SMACrossover

strategies: dict = {
    'Price Threshold': {
            'class': PriceThreshold,
            'buy_sell_keyword': 'price'
        },
    'RSI Threshold': {
            'class': RSIThreshold,
            'buy_sell_keyword': 'RSI'
        },
    'SMA Crossover': {
            'class': SMACrossover,
            'buy_sell_keyword': 'SMA'
        },
    }