import pandas as pd


class OrderBlockIndicator:
    def __init__(self, lookback=5):
        self.lookback = lookback

    def find_order_blocks(self, data):
        order_blocks = []
        for i in range(len(data) - self.lookback):
            high = data['high'][i:i + self.lookback].max()
            low = data['low'][i:i + self.lookback].min()
            order_blocks.append((high, low))

        # Add NaN values for the first lookback rows
        order_blocks = [(None, None)] * self.lookback + order_blocks
        df = pd.DataFrame(order_blocks, columns=['order_block_high', 'order_block_low'], index=data.index)
        return df['order_block_high'], df['order_block_low']
