from ta.base.abstract_indicator import AbstractIndicator
from ta.base.ma import MovingAverage


class StochasticOscillator(AbstractIndicator):
    NAME = 'STOCH'

    def __init__(self, stochastic_period=14, k_period=3, d_period=3):
        super().__init__()
        self.stochastic_period = stochastic_period
        self.k_period_ma = MovingAverage(k_period)
        self.d_period_ma = MovingAverage(d_period)

    def call(self, data):
        high_rolling = data['high'].rolling(window=self.stochastic_period)
        low_rolling = data['low'].rolling(window=self.stochastic_period)

        high_low_range = high_rolling.max() - low_rolling.min()
        close_low_range = data['close'] - low_rolling.min()

        raw_percent_k = (close_low_range / high_low_range) * 100

        percent_k = self.k_period_ma.sma(raw_percent_k)
        percent_d = self.d_period_ma.sma(percent_k)

        return percent_k, percent_d
