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

        order_block_high, order_block_low = high_rolling.max(), low_rolling.min()

        df = pd.concat([order_block_high, order_block_low], axis=1)
        df.columns = ['order_block_high', 'order_block_low']
        df.iloc[:self.lookback] = None

        return df['order_block_high'], df['order_block_low']
