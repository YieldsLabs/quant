from .base.base_strategy import BaseStrategy
from ta.patterns.extreme_euphoria import ExtremeEuphoria
from ta.volatility.bbands import BollingerBands


class ExtremeEuphoriaBollingerBands(BaseStrategy):
    NAME = "EEBB"

    def __init__(self, sma_period=20, stdev_multi=2):
        indicators = [
            (BollingerBands(sma_period, stdev_multi), ('upper_band', 'middle_band', 'lower_band'))
        ]
        patterns = [
            (ExtremeEuphoria(), (ExtremeEuphoria.bullish_column(), ExtremeEuphoria.bearish_column()))
        ]
        super().__init__(indicators, patterns)

    def _generate_buy_signal(self, data):
        last_row = data.iloc[-1]
        buy_signal = last_row[ExtremeEuphoria.bullish_column()] and (
            last_row['close'] <= last_row['lower_band'])
        return buy_signal

    def _generate_sell_signal(self, data):
        last_row = data.iloc[-1]
        sell_signal = last_row[ExtremeEuphoria.bearish_column()] and (
            last_row['close'] >= last_row['upper_band'])
        return sell_signal
