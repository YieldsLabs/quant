from shared.meta_label import meta_label
from ta.base.abstract_indicator import AbstractIndicator
from ta.base.ma import MovingAverage


@meta_label
class FairValueGap(AbstractIndicator):
    NAME = "FVG"

    def __init__(self, lookback=15):
        super().__init__()
        self.ma = MovingAverage(window=lookback)

    def call(self, data):
        fair_values = data['close']

        fair_value_mean = self.ma.sma(fair_values)
        fair_value_gap = fair_values - fair_value_mean

        fair_value_gap.iloc[:self.ma.window] = None

        return fair_value_gap
