from ta.BBIndicator import BBIndicator
from strategy.AbstractStrategy import AbstractStrategy
from patters.EngulfingPattern import EngulfingPattern


class BollingerEngulfing(AbstractStrategy):
    def __init__(self, bb_period=20, bb_std_dev=2):
        super().__init__()
        self.bb = BBIndicator(sma_period=bb_period, multiplier=bb_std_dev)

    def add_indicators(self, data):
        data = data.copy()
        data['upper_band'], data['lower_band'] = self.bb.bb(data)

        data['bullish_engulfing'] = EngulfingPattern.bullish(data)
        data['bearish_engulfing'] = EngulfingPattern.bearish(data)

        return data

    def entry(self, data):
        if len(data) < 2:
            return False, False

        data = self.add_indicators(data)
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
        return 'BollingerEngulfing'
