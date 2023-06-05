from ta.base.abstract_indicator import AbstractIndicator
from ta.base.ma import MovingAverage


class SimpleMA(AbstractIndicator):
    NAME = 'SMA'

    def __init__(self, period=100):
        super().__init__()
        self.ma = MovingAverage(period)
        self.sma_period = period

    def call(self, data, column='close'):
        return self.ma.sma(data[column])
