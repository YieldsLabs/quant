from ta.base.abstract_indicator import AbstractIndicator
from ta.base.ma import MovingAverage


class MACD(AbstractIndicator):
    NAME = 'MACD'

    def __init__(self, short_period=12, long_period=26, signal_period=9):
        super().__init__()
        self.fast_ema = MovingAverage(short_period)
        self.slow_ema = MovingAverage(long_period)
        self.signal_ema = MovingAverage(signal_period)

    def call(self, data):
        close = data['close']
        
        ema_fast = self.fast_ema.ema(close)
        ema_slow = self.slow_ema.ema(close)

        macd = ema_fast - ema_slow
        signal_line = self.signal_ema.ema(macd)
        histogram = macd - signal_line

        return macd, signal_line, histogram
