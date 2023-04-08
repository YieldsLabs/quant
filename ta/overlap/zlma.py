from shared.meta_label import meta_label
from ta.base.abstract_indicator import AbstractIndicator
from ta.base.ma import MovingAverage


@meta_label
class ZeroLagEMA(AbstractIndicator):
    NAME = 'ZLMA'

    def __init__(self, window=5):
        super().__init__()
        self.ma = MovingAverage(window=window)
        self.window = window

    def call(self, data, column='close'):
        ema = self.ma.ema(data[column])
        lag = (self.window - 1) // 2
        shifted_series = data[column].shift(-lag)
        zlema = 2 * ema - self.ma.ema(shifted_series)
        return zlema
