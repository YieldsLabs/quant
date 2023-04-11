import pandas as pd

from ta.base.abstract_indicator import AbstractIndicator


class OrderBlock(AbstractIndicator):
    NAME = "OB"

    def __init__(self, lookback=25):
        super().__init__()
        self.lookback = lookback

    def call(self, data):
        high_rolling = data['high'].rolling(self.lookback, min_periods=self.lookback)
        low_rolling = data['low'].rolling(self.lookback, min_periods=self.lookback)

        order_block_high = high_rolling.max()
        order_block_low = low_rolling.min()

        order_block_high.iloc[:self.lookback] = None
        order_block_low.iloc[:self.lookback] = None

        return order_block_high, order_block_low
