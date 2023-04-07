from strategy.abstract_strategy import AbstractStrategy
from ta.volatility.bbands import BollingerBands
from ta.patterns.extreme_euphoria import ExtremeEuphoria


class ExtremeEuphoriaBBStrategy(AbstractStrategy):
    def __init__(self, sma_period=20, multiplier=2):
        super().__init__()
        self.bb_indicator = BollingerBands(sma_period, multiplier)

    def _add_indicators(self, ohlcv):
        data = ohlcv.copy()

        data['upper_band'], _, data['lower_band'] = self.bb_indicator.call(data)
        data['bullish_extreme_euphoria'] = ExtremeEuphoria.bullish(
            data)
        data['bearish_extreme_euphoria'] = ExtremeEuphoria.bearish(
            data)
        return data

    def entry(self, ohlcv):
        if len(ohlcv) < 6:
            return False, False

        data = self._add_indicators(ohlcv)

        last_row = data.iloc[-1]

        buy_signal = last_row['bullish_extreme_euphoria'] and (
            last_row['close'] <= last_row['lower_band'])
        sell_signal = last_row['bearish_extreme_euphoria'] and (
            last_row['close'] >= last_row['upper_band'])

        return buy_signal, sell_signal

    def exit(self, ohlcv):
        pass

    def __str__(self) -> str:
        return f'_STRATEGYEXTREMEEUPHORIA{self.bb_indicator}{ExtremeEuphoria()}'
