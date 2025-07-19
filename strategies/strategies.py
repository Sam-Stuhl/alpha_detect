from .price_threshold import PriceThreshold
from .rsi_threshold import RSIThreshold
from .sma_crossover import SMACrossover

strategies: dict = {
    'Price Threshold': PriceThreshold,
    'RSI Threshold': RSIThreshold,
    'SMA Crossover': SMACrossover,
    }