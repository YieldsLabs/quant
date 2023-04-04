from ta.indicators.base.abstract_indicator import AbstractIndicator
from ta.indicators.base.ma import MovingAverage


class ZeroLagEMAIndicator(AbstractIndicator):
    def __init__(self, window=5):
        self.window = window
        self.ma = MovingAverage(window=window)

    def call(self, data, column='close'):
        ema = self.ma.ema(data[column])
        lag = (self.window - 1) // 2
        shifted_series = data[column].shift(-lag)
        zlema = 2 * ema - self.ma.ema(shifted_series)
        return zlema

    def __str__(self) -> str:
        return f'ZeroLagEMAIndicator(window={self.window})'
