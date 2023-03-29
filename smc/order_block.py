import pandas as pd


class OrderBlockIndicator:
    def __init__(self, lookback=25):
        self.lookback = lookback

    def find_order_blocks(self, data):
        high_rolling = data['high'].rolling(self.lookback, min_periods=self.lookback)
        low_rolling = data['low'].rolling(self.lookback, min_periods=self.lookback)

        order_blocks = list(zip(high_rolling.max(), low_rolling.min()))
        
        df = pd.DataFrame(order_blocks, columns=['order_block_high', 'order_block_low'], index=data.index)
        
        df.iloc[:self.lookback] = None
        
        return df['order_block_high'], df['order_block_low']
