from ta.base.abstract_indicator import AbstractIndicator
from ta.base.ma import MovingAverage


class AwesomeOscillator(AbstractIndicator):
    NAME = 'AO'

    def __init__(self, ao_short_period=5, ao_long_period=34):
        super().__init__()
        self.short_period_ma = MovingAverage(ao_short_period)
        self.long_period_ma = MovingAverage(ao_long_period)

        # known issue with meta labels
        self.ao_short_period = ao_short_period
        self.ao_long_period = ao_long_period

    def call(self, data):
        median_price = (data['high'] + data['low']) / 2

        return self.short_period_ma.sma(median_price) - self.long_period_ma.sma(median_price)
