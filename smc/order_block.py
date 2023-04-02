import pandas as pd


class OrderBlockIndicator:
    def __init__(self, lookback=25):
        self.lookback = lookback

    def find_order_blocks(self, data):
        high_rolling = data['high'].rolling(self.lookback, min_periods=self.lookback)
        low_rolling = data['low'].rolling(self.lookback, min_periods=self.lookback)

        order_block_high = high_rolling.max()
        order_block_low = low_rolling.min()

        df = pd.concat([order_block_high, order_block_low], axis=1)
        df.columns = ['order_block_high', 'order_block_low']
        df.iloc[:self.lookback] = None

        return df['order_block_high'], df['order_block_low']
