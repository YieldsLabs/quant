import numpy as np


class MovingAverageIndicator:
    def __init__(self, window=20):
        self.window = window

    def sma(self, data):
        return data.rolling(window=self.window).mean()

    def ema(self, data):
        return data.ewm(span=self.window).mean()

    def smma(self, data):
        return data.ewm(alpha=1/self.window).mean()

    def wma(self, data):
        weights = np.arange(1, self.window+1)
        return data.rolling(window=self.window).apply(lambda x: np.dot(x, weights)/weights.sum(), raw=True)

    def vwma(self, data, volume):
        return (data * volume).rolling(window=self.window).sum() / volume.rolling(window=self.window).sum()
    
    def __str__(self) -> str:
        return f'MovingAverageIndicator(window={self.window})'

