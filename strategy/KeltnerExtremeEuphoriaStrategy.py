from indicators.KeltnerChannelsIndicator import KeltnerChannelsIndicator
from ta.MovingAverageIndicator import MovingAverageIndicator
from patters.ExtremeEuphoriaPattern import ExtremeEuphoriaPattern
from strategy.AbstractStrategy import AbstractStrategy

class KeltnerExtremeEuphoriaStrategy(AbstractStrategy):
    def __init__(self, ema_period=20, atr_period=14, multiplier=2, sma_period=50):
        super().__init__()
        self.keltner_channels = KeltnerChannelsIndicator(ema_period, atr_period, multiplier)
        self.sma = MovingAverageIndicator(sma_period)

    def add_indicators(self, data):
        data = data.copy()
        data['upper_band'], _, data['lower_band'] = self.keltner_channels.keltner_channels(data)
        data['sma'] = self.sma.sma(data['close'])
        data['extreme_euphoria_bullish'] = ExtremeEuphoriaPattern.bullish(data)
        data['extreme_euphoria_bearish'] = ExtremeEuphoriaPattern.bearish(data)

        return data

    def entry(self, data):
        if len(data) < 2:
            return False, False

        data = self.add_indicators(data)
        current_row = data.iloc[-1]

        buy_signal = (
            current_row['close'] <= current_row['lower_band'] and
            current_row['extreme_euphoria_bullish'] and
            current_row['close'] > current_row['sma']
        )
        sell_signal = (
            current_row['close'] >= current_row['upper_band'] and
            current_row['extreme_euphoria_bearish'] and
            current_row['close'] < current_row['sma']
        )

        return buy_signal, sell_signal

    def __str__(self) -> str:
        return 'KeltnerExtremeEuphoriaStrategy'
