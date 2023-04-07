
from strategy.abstract_strategy import AbstractStrategy
from ta.patterns.engulfing import Engulfing
from ta.volatility.bbands import BollingerBands


class BollingerEngulfing(AbstractStrategy):
    def __init__(self, sma_period=20, multiplier=2):
        super().__init__()
        self.bb = BollingerBands(sma_period=sma_period, multiplier=multiplier)

    def _add_indicators(self, ohlcv):
        data = ohlcv.copy()
        data['upper_band'], _, data['lower_band'] = self.bb.call(data)
        data['bullish_engulfing'] = Engulfing.bullish(data)
        data['bearish_engulfing'] = Engulfing.bearish(data)

        return data

    def entry(self, ohlcv):
        if len(ohlcv) < 2:
            return False, False

        data = self._add_indicators(ohlcv)

        current_row = data.iloc[-1]

        buy_signal = (
            current_row['close'] <= current_row['lower_band']
            and current_row['bullish_engulfing']
        )
        sell_signal = (
            current_row['close'] >= current_row['upper_band']
            and current_row['bearish_engulfing']
        )

        return buy_signal, sell_signal

    def exit(self, ohlcv):
        pass

    def __str__(self) -> str:
        return f'_STRATEGYBBENGULFING{self.bb}{Engulfing()}'
