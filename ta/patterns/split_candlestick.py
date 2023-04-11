import numpy as np

from ta.patterns.abstract_pattern import AbstractPattern


class SplitCandlestick(AbstractPattern):
    NAME = 'SPLITCANDLESTICK'

    @staticmethod
    def bullish(data):
        return (
            (data['close'].shift(1) < data['open'].shift(1))
            & (data['open'].shift(1) < data['high'].shift(1))
            & np.isclose(data['close'].shift(1), data['low'].shift(1))
            & (data['close'] > data['open'])
            & np.isclose(data['close'], data['high'])
            & (data['open'] > data['low'])
            & (data['close'] > data['open'].shift(1))
        )

    @staticmethod
    def bearish(data):
        return (
            (data['close'].shift(1) > data['open'].shift(1))
            & (data['open'].shift(1) > data['low'].shift(1))
            & np.isclose(data['close'].shift(1), data['high'].shift(1))
            & (data['close'] < data['open'])
            & np.isclose(data['close'], data['low'])
            & (data['open'] < data['high'])
            & (data['close'] < data['open'].shift(1))
        )
