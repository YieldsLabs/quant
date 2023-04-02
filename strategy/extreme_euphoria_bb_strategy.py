from typing import Type
from patterns.extreme_euphoria_pattern import ExtremeEuphoriaPattern
from shared.ohlcv_context import OhlcvContext
from strategy.abstract_strategy import AbstractStrategy
from ta.bb_indicator import BBIndicator


class ExtremeEuphoriaBBStrategy(AbstractStrategy):
    def __init__(self, ohlcv: Type[OhlcvContext], sma_period=20, multiplier=2):
        super().__init__(ohlcv)
        self.bb_indicator = BBIndicator(sma_period, multiplier)
        self.extreme_euphoria_finder = ExtremeEuphoriaPattern()

    def _add_indicators(self, data):
        data['upper_band'], data['lower_band'] = self.bb_indicator.bb(data)
        data['bullish_extreme_euphoria'] = self.extreme_euphoria_finder.bullish(
            data)
        data['bearish_extreme_euphoria'] = self.extreme_euphoria_finder.bearish(
            data)
        return data

    def entry(self):
        data = self.ohlcv_context.ohlcv

        if len(data) < 6:
            return False, False

        data = self._add_indicators(data)

        last_row = data.iloc[-1]

        buy_signal = last_row['bullish_extreme_euphoria'] and (
            last_row['close'] <= last_row['lower_band'])
        sell_signal = last_row['bearish_extreme_euphoria'] and (
            last_row['close'] >= last_row['upper_band'])

        return buy_signal, sell_signal

    def __str__(self) -> str:
        return f'ExtremeEuphoriaBBStrategy(bb_indicator={self.bb_indicator})'
