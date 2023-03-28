from smc.order_block import OrderBlockIndicator
from ta.rsi_indicator import RSIIndicator
from strategy.abstract_strategy import AbstractStrategy

class StructuredDurationStrategy(AbstractStrategy):
    def __init__(self, upper_barrier=80, lower_barrier=20, lookback_rsi=5, lookback_order_block=5):
        super().__init__()
        self.upper_barrier = upper_barrier
        self.lower_barrier = lower_barrier
        self.lookback_rsi = lookback_rsi
        self.lookback_order_block = lookback_order_block

        self.rsi_indicator = RSIIndicator(lookback_rsi)
        self.order_block_indicator = OrderBlockIndicator(lookback_order_block)

    def add_indicators(self, data):
        data = data.copy()
        data['rsi'] = self.rsi_indicator.rsi(data['close'])
        data['order_block_high'], data['order_block_low'] = self.order_block_indicator.find_order_blocks(data)
        return data

    def entry(self, data):
        if len(data) < max(self.lookback_rsi + 1, self.lookback_order_block):
            return False, False

        data = self.add_indicators(data)

        last_row = data.iloc[-1]
        previous_rows = data.iloc[-(self.lookback_rsi + 1):-1]

        buy_signal = (
            last_row['rsi'] > self.lower_barrier
            and last_row['low'] < data.iloc[-2]['low']
            and all(previous_rows['rsi'] < self.lower_barrier)
            and last_row['low'] < last_row['order_block_low']
        )

        sell_signal = (
            last_row['rsi'] < self.upper_barrier
            and last_row['high'] > data.iloc[-2]['high']
            and all(previous_rows['rsi'] > self.upper_barrier)
            and last_row['high'] > last_row['order_block_high']
        )

        return buy_signal, sell_signal

    def __str__(self) -> str:
        return f'StructuredDurationIndicatorStrategy(upper_barrier={self.upper_barrier}, lower_barrier={self.lower_barrier})'
