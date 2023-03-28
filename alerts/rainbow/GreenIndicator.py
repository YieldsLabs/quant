import pandas as pd
from ta.momentum import RSIIndicator


class GreenIndicator:
    def __init__(self, lookback=5, lookback_rsi=13):
        self.lookback = lookback
        self.lookback_rsi = lookback_rsi

    def alert(self, ohlcv):
        data = ohlcv.copy()

        data['rsi'] = RSIIndicator(
            data['close'], window=self.lookback_rsi).rsi()
        data['rsi_slope'] = (
            data['rsi'] - data['rsi'].shift(self.lookback)) / self.lookback

        buy = (
            data['rsi_slope'] > 0 and
            data['rsi_slope'].shift(1) < 0 and
            data['rsi'] < 25
        )

        sell = (
            data['rsi_slope'] < 0 and
            data['rsi_slope'].shift(1) > 0 and
            data['rsi'] > 75
        )

        return buy, sell
