from strategy.abstract_strategy import AbstractStrategy
from ta.indicators.base.ma import MovingAverage
from ta.patterns.kangaroo_tail_pattern import KangarooTailPattern


class KangarooTailStrategy(AbstractStrategy):
    def __init__(self, lookback=200, sma_period=100):
        super().__init__()
        self.lookback = lookback
        self.sma_period = sma_period
        self.ma = MovingAverage(sma_period)

    def _add_indicators(self, ohlcv):
        data = ohlcv.copy()

        data['sma'] = self.ma.smma(data['close'])
        data['bullish_kangaroo_tail'] = KangarooTailPattern.bullish(data, self.lookback)
        data['bearish_kangaroo_tail'] = KangarooTailPattern.bearish(data, self.lookback)

        return data

    def entry(self, ohlcv):
        if len(ohlcv) < max(3, self.sma_period):
            return False, False

        data = self._add_indicators(ohlcv)

        current_row = data.iloc[-1]

        buy_signal = (
            current_row['bullish_kangaroo_tail']
            and current_row['close'] > current_row['sma']
        )
        sell_signal = (
            current_row['bearish_kangaroo_tail']
            and current_row['close'] < current_row['sma']
        )

        return buy_signal, sell_signal

    def exit(self, ohlcv):
        pass

    def __str__(self) -> str:
        return f'KangarooTailStrategy(lookback={self.lookback}, sma_period={self.sma_period})'
