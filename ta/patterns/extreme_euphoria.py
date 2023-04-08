import numpy as np
from ta.patterns.abstract_pattern import AbstractPattern


class ExtremeEuphoria(AbstractPattern):
    NAME = 'EXTREMEEUPHORIA'

    @staticmethod
    def bullish(data):
        bullish_extreme_euphoria = (
            (data['close'].shift(5) < data['open'].shift(5))
            & (data['close'].shift(4) < data['open'].shift(4))
            & (data['close'].shift(3) < data['open'].shift(3))
            & (data['close'].shift(2) < data['open'].shift(2))
            & (data['close'].shift(1) < data['open'].shift(1))
            & (np.abs(data['close'].shift(1) - data['open'].shift(1)) > np.abs(data['close'].shift(2) - data['open'].shift(2)))
            & (np.abs(data['close'].shift(2) - data['open'].shift(2)) > np.abs(data['close'].shift(3) - data['open'].shift(3)))
            & (np.abs(data['close'].shift(3) - data['open'].shift(3)) > np.abs(data['close'].shift(4) - data['open'].shift(4)))
        )
        return bullish_extreme_euphoria

    @staticmethod
    def bearish(data):
        bearish_extreme_euphoria = (
            (data['close'].shift(5) > data['open'].shift(5))
            & (data['close'].shift(4) > data['open'].shift(4))
            & (data['close'].shift(3) > data['open'].shift(3))
            & (data['close'].shift(2) > data['open'].shift(2))
            & (data['close'].shift(1) > data['open'].shift(1))
            & (np.abs(data['close'].shift(1) - data['open'].shift(1)) > np.abs(data['close'].shift(2) - data['open'].shift(2)))
            & (np.abs(data['close'].shift(2) - data['open'].shift(2)) > np.abs(data['close'].shift(3) - data['open'].shift(3)))
            & (np.abs(data['close'].shift(3) - data['open'].shift(3)) > np.abs(data['close'].shift(4) - data['open'].shift(4)))
        )
        return bearish_extreme_euphoria
