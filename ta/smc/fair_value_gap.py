from ta.base.abstract_indicator import AbstractIndicator
from ta.base.ma import MovingAverage


class FairValueGap(AbstractIndicator):
    def __init__(self, lookback=15):
        self.ma = MovingAverage(window=lookback)
        self.lookback = lookback

    def call(self, data):
        fair_values = data['close']

        fair_value_mean = self.ma.sma(fair_values)
        fair_value_gap = fair_values - fair_value_mean

        fair_value_gap.iloc[:self.lookback] = None

        return fair_value_gap

    def __str__(self) -> str:
        return f'_FVG_{self.lookback}{self.ma}'
