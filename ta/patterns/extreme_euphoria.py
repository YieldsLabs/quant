import numpy as np
from ta.patterns.abstract_pattern import AbstractPattern


class ExtremeEuphoria(AbstractPattern):
    NAME = 'EXTREMEEUPHORIA'

    def bullish(self, data):
        return (
            (data['close'].shift(5) < data['open'].shift(5))
            & (data['close'].shift(4) < data['open'].shift(4))
            & (data['close'].shift(3) < data['open'].shift(3))
            & (data['close'].shift(2) < data['open'].shift(2))
            & (data['close'].shift(1) < data['open'].shift(1))
            & (np.abs(data['close'].shift(1) - data['open'].shift(1)) > np.abs(data['close'].shift(2) - data['open'].shift(2)))
            & (np.abs(data['close'].shift(2) - data['open'].shift(2)) > np.abs(data['close'].shift(3) - data['open'].shift(3)))
            & (np.abs(data['close'].shift(3) - data['open'].shift(3)) > np.abs(data['close'].shift(4) - data['open'].shift(4)))
        )

    def bearish(self, data):
        return (
            (data['close'].shift(5) > data['open'].shift(5))
            & (data['close'].shift(4) > data['open'].shift(4))
            & (data['close'].shift(3) > data['open'].shift(3))
            & (data['close'].shift(2) > data['open'].shift(2))
            & (data['close'].shift(1) > data['open'].shift(1))
            & (np.abs(data['close'].shift(1) - data['open'].shift(1)) > np.abs(data['close'].shift(2) - data['open'].shift(2)))
            & (np.abs(data['close'].shift(2) - data['open'].shift(2)) > np.abs(data['close'].shift(3) - data['open'].shift(3)))
            & (np.abs(data['close'].shift(3) - data['open'].shift(3)) > np.abs(data['close'].shift(4) - data['open'].shift(4)))
        )
