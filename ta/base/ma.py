import numpy as np
from pandas import Series

from shared.meta_label.meta_label import meta_label


@meta_label
class MovingAverage:
    def __init__(self, sma_period=20):
        self.sma_period = int(sma_period)

    def sma(self, close: Series):
        return close.rolling(window=self.sma_period).mean()

    def ema(self, close: Series):
        return close.ewm(span=self.sma_period).mean()

    def smma(self, close: Series):
        return close.ewm(alpha=1 / self.sma_period).mean()

    def wma(self, close: Series):
        weights = np.arange(1, self.sma_period + 1)
        return close.rolling(window=self.sma_period).apply(lambda x: np.dot(x, weights) / weights.sum(), raw=True)

    def vwma(self, close: Series, volume: Series):
        return (close * volume).rolling(window=self.sma_period).sum() / volume.rolling(window=self.sma_period).sum()
