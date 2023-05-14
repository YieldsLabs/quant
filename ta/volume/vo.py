from ta.base.abstract_indicator import AbstractIndicator

from ta.base.ma import MovingAverage


class VolumeOscillator(AbstractIndicator):
    NAME = 'VO'

    def __init__(self, short_period=5, long_period=14):
        super().__init__()
        self.short_sma = MovingAverage(short_period)
        self.long_sma = MovingAverage(long_period)

        self.short_period = short_period
        self.long_period = long_period

    def call(self, ohlcv):
        volume = ohlcv['volume']

        short_sma = self.short_sma.sma(volume)
        long_sma = self.long_sma.sma(volume)

        vo = (short_sma - long_sma) / long_sma * 100

        return vo
