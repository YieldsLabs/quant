

from ta.indicators.base.abstract_indicator import AbstractIndicator
from ta.indicators.base.ma import MovingAverage


class MACDIndicator(AbstractIndicator):
    def __init__(self, short_period=12, long_period=26, signal_period=9):
        self.fast_ema = MovingAverage(window=short_period)
        self.slow_ema = MovingAverage(window=long_period)
        self.signal_ema = MovingAverage(window=signal_period)

    def call(self, data):
        ema_fast = self.fast_ema.ema(data['close'])
        ema_slow = self.fast_ema.ema(data['close'])

        macd = ema_fast - ema_slow
        signal_line = self.signal_ema.ema(macd)
        histogram = macd - signal_line

        return macd, signal_line, histogram

    def __str__(self) -> str:
        return f'MACDIndicator(fast_ema={self.fast_ema}, slow_ema={self.slow_ema}, signal_period={self.signal_period})'
