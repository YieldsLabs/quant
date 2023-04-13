from ta.base.abstract_indicator import AbstractIndicator
from ta.base.ma import MovingAverage


class FairValueGap(AbstractIndicator):
    NAME = "FVG"

    def __init__(self, sma_period=15):
        super().__init__()
        self.ma = MovingAverage(sma_period)
        self.sma_period = sma_period

    def call(self, data):
        fair_values = data['close']

        fair_value_mean = self.ma.sma(fair_values)
        fair_value_gap = fair_values - fair_value_mean

        fair_value_gap.iloc[:self.ma.sma_period] = None

        return fair_value_gap
