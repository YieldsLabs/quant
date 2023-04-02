from argon2 import Type
from patterns.engulfing_pattern import EngulfingPattern
from shared.ohlcv_context import OhlcvContext
from ta.bb_indicator import BBIndicator
from strategy.abstract_strategy import AbstractStrategy

class BollingerEngulfing(AbstractStrategy):
    def __init__(self, ohlcv: Type[OhlcvContext], sma_period=20, multiplier=2):
        super().__init__(ohlcv)
        self.bb = BBIndicator(sma_period=sma_period, multiplier=multiplier)

    def _add_indicators(self, data):
        data['upper_band'], data['lower_band'] = self.bb.bb(data)
        data['bullish_engulfing'] = EngulfingPattern.bullish(data)
        data['bearish_engulfing'] = EngulfingPattern.bearish(data)

        return data

    def entry(self):
        data = self.ohlcv_context.ohlcv

        if len(data) < 2:
            return False, False
        
        data = self._add_indicators(data)

        current_row = data.iloc[-1]

        buy_signal = (
            current_row['close'] <= current_row['lower_band'] and
            current_row['bullish_engulfing']
        )
        sell_signal = (
            current_row['close'] >= current_row['upper_band'] and
            current_row['bearish_engulfing']
        )

        return buy_signal, sell_signal

    def __str__(self) -> str:
        return f'BollingerEngulfing(bb={self.bb})'
