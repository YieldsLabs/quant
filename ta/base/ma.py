import numpy as np
from pandas import Series

from shared.meta_label.meta_label import meta_label


@meta_label
class MovingAverage:
    def __init__(self, window=20):
        self.window = window

    def sma(self, close: Series):
        return close.rolling(window=self.window).mean()

    def ema(self, close: Series):
        return close.ewm(span=self.window).mean()

    def smma(self, close: Series):
        return close.ewm(alpha=1 / self.window).mean()

    def wma(self, close: Series):
        weights = np.arange(1, self.window + 1)
        return close.rolling(window=self.window).apply(lambda x: np.dot(x, weights) / weights.sum(), raw=True)

    def vwma(self, close: Series, volume: Series):
        return (close * volume).rolling(window=self.window).sum() / volume.rolling(window=self.window).sum()
