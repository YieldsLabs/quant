import numpy as np
import pandas as pd

from ta.base.abstract_indicator import AbstractIndicator


class AverageTrueRange(AbstractIndicator):
    NAME = 'ATR'

    def __init__(self, period=14, smoothing='RMA'):
        super().__init__()
        self.period = period
        self.smoothing = smoothing

    def call(self, ohlcv):
        high = ohlcv['high'].to_numpy()
        low = ohlcv['low'].to_numpy()
        close = ohlcv['close'].to_numpy()

        previous_close = np.roll(close, 1)
        previous_close[0] = close[0]

        true_range = np.maximum(high - low, np.maximum(np.abs(high - previous_close), np.abs(low - previous_close)))

        if self.smoothing == 'RMA':
            atr = pd.Series(true_range).ewm(span=self.period, adjust=False).mean()
        elif self.smoothing == 'WILDER':
            atr = np.zeros_like(true_range)
            atr[self.period] = np.mean(true_range[1:self.period + 1])

            for i in range(self.period + 1, len(atr)):
                atr[i] = (atr[i - 1] * (self.period - 1) + true_range[i]) / self.period
        else:
            atr = pd.Series(true_range).rolling(window=self.period).mean()

        return pd.Series(atr, index=ohlcv.index)
