from .base.base_strategy import BaseStrategy
from ta.overlap.zlma import ZeroLagEMA
from ta.patterns.kangaroo_tail import KangarooTail


class KangarooTailZLMA(BaseStrategy):
    NAME = "KTZLMA"

    def __init__(self, slow_sma_period=100, lookback=100):
        indicators = [
            (ZeroLagEMA(slow_sma_period), ZeroLagEMA.NAME)
        ]
        patterns = [
            (KangarooTail(lookback), (KangarooTail.bullish_column(), KangarooTail.bearish_column()))
        ]
        super().__init__(indicators, patterns)

    def _generate_buy_signal(self, data):
        current_row = data.iloc[-1]

        buy_signal = (
            current_row[KangarooTail.bullish_column()]
            and current_row['close'] > current_row[ZeroLagEMA.NAME]
        )

        return buy_signal

    def _generate_sell_signal(self, data):
        current_row = data.iloc[-1]

        sell_signal = (
            current_row[KangarooTail.bearish_column()]
            and current_row['close'] < current_row[ZeroLagEMA.NAME]
        )

        return sell_signal
