from ta.MovingAverageIndicator import MovingAverageIndicator
from patterns.KangarooTailPattern import KangarooTailPattern
from strategy.AbstractStrategy import AbstractStrategy

class KangarooTailStrategy(AbstractStrategy):
    def __init__(self, lookback=200, sma_period=100):
        super().__init__()
        self.lookback = lookback
        self.sma_period = sma_period
        self.ma = MovingAverageIndicator(sma_period)

    def add_indicators(self, data):
        data = data.copy()
        data['sma'] = self.ma.smma(data['close'])
        data['bullish_kangaroo_tail'] = KangarooTailPattern.bullish(data, self.lookback)
        data['bearish_kangaroo_tail'] = KangarooTailPattern.bearish(data, self.lookback)

        return data

    def entry(self, data):
        if len(data) < max(3, self.sma_period):
            return False, False

        data = self.add_indicators(data)
        current_row = data.iloc[-1]

        buy_signal = (
            current_row['bullish_kangaroo_tail'] and
            current_row['close'] > current_row['sma']
        )
        sell_signal = (
            current_row['bearish_kangaroo_tail'] and
            current_row['close'] < current_row['sma']
        )

        return buy_signal, sell_signal

    def __str__(self) -> str:
        return f'KangarooTailStrategy(lookback={self.lookback}, sma_period={self.sma_period})'
