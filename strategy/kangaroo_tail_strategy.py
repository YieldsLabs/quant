from strategy.abstract_strategy import AbstractStrategy
from ta.base.ma import MovingAverage
from ta.patterns.kangaroo_tail import KangarooTail


class KangarooTailStrategy(AbstractStrategy):
    def __init__(self, lookback=200, sma_period=100):
        super().__init__()
        self.ma = MovingAverage(sma_period)
        self.lookback = lookback

    def _add_indicators(self, ohlcv):
        data = ohlcv.copy()

        data['sma'] = self.ma.smma(data['close'])
        data['bullish_kangaroo_tail'] = KangarooTail.bullish(data, self.lookback)
        data['bearish_kangaroo_tail'] = KangarooTail.bearish(data, self.lookback)

        return data

    def entry(self, ohlcv):
        if len(ohlcv) < max(3, self.ma.window):
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
        return f'_KANGAROOTAILSTRATEGY_{self.lookback}{self.ma}{KangarooTail()}'
