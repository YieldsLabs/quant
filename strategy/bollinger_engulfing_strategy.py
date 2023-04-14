from .base.base_strategy import BaseStrategy
from ta.patterns.engulfing import Engulfing
from ta.volatility.bbands import BollingerBands


class BollingerBandsEngulfing(BaseStrategy):
    NAME = "BBE"

    def __init__(self, sma_period=20, stdev_multi=2):
        indicators = [
            (BollingerBands(sma_period, stdev_multi), ('upper_band', 'middle_band', 'lower_band'))
        ]
        patterns = [
            (Engulfing(), (Engulfing.bullish_column(), Engulfing.bearish_column()))
        ]

        super().__init__(indicators, patterns)

    def _generate_buy_signal(self, data):
        return (
            data['close'].iloc[-1] <= data['lower_band'].iloc[-1]
            and data[Engulfing.bullish_column()].iloc[-1]
        )

    def _generate_sell_signal(self, data):
        return (
            data['close'].iloc[-1] >= data['upper_band'].iloc[-1]
            and data[Engulfing.bearish_column()].iloc[-1]
        )
