import pandas as pd
from ta.base.abstract_indicator import AbstractIndicator
from ta.base.ma import MovingAverage


class ZeroLagEMA(AbstractIndicator):
    NAME = 'ZLMA'

    def __init__(self, slow_sma_period=5):
        super().__init__()
        self.ma = MovingAverage(sma_period=slow_sma_period)
        self.slow_sma_period = slow_sma_period

    def call(self, data, column='close'):
        close_values = data[column].values
        ema = self.ma.ema(pd.Series(close_values, index=data.index))
        lag = (self.slow_sma_period - 1) // 2
        shifted_series = pd.Series(close_values, index=data.index).shift(-lag)
        zlema = 2 * ema - self.ma.ema(shifted_series)
        return zlema
