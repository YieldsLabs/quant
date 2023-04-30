import numpy as np
from .abstract_pattern import AbstractPattern


class ExtremeEuphoria(AbstractPattern):
    NAME = 'EXTREMEEUPHORIA'

    def bullish(self, data):
        consecutive_bearish_candles = (
            (data['close'].shift(5) < data['open'].shift(5))
            & (data['close'].shift(4) < data['open'].shift(4))
            & (data['close'].shift(3) < data['open'].shift(3))
            & (data['close'].shift(2) < data['open'].shift(2))
            & (data['close'].shift(1) < data['open'].shift(1))
        )

        increasing_bearish_body = (
            (np.abs(data['close'].shift(1) - data['open'].shift(1)) > np.abs(data['close'].shift(2) - data['open'].shift(2)))
            & (np.abs(data['close'].shift(2) - data['open'].shift(2)) > np.abs(data['close'].shift(3) - data['open'].shift(3)))
            & (np.abs(data['close'].shift(3) - data['open'].shift(3)) > np.abs(data['close'].shift(4) - data['open'].shift(4)))
        )

        return consecutive_bearish_candles & increasing_bearish_body

    def bearish(self, data):
        consecutive_bullish_candles = (
            (data['close'].shift(5) > data['open'].shift(5))
            & (data['close'].shift(4) > data['open'].shift(4))
            & (data['close'].shift(3) > data['open'].shift(3))
            & (data['close'].shift(2) > data['open'].shift(2))
            & (data['close'].shift(1) > data['open'].shift(1))
        )

        increasing_bullish_body = (
            (np.abs(data['close'].shift(1) - data['open'].shift(1)) > np.abs(data['close'].shift(2) - data['open'].shift(2)))
            & (np.abs(data['close'].shift(2) - data['open'].shift(2)) > np.abs(data['close'].shift(3) - data['open'].shift(3)))
            & (np.abs(data['close'].shift(3) - data['open'].shift(3)) > np.abs(data['close'].shift(4) - data['open'].shift(4)))
        )

        return consecutive_bullish_candles & increasing_bullish_body
