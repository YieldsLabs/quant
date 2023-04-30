import numpy as np

from .abstract_pattern import AbstractPattern


class SplitCandlestick(AbstractPattern):
    NAME = 'SPLITCANDLESTICK'

    def bullish(self, data):
        previous_candle = (
            (data['close'].shift(1) < data['open'].shift(1))
            & (data['open'].shift(1) < data['high'].shift(1))
            & np.isclose(data['close'].shift(1), data['low'].shift(1))
        )

        current_candle = (
            (data['close'] > data['open'])
            & np.isclose(data['close'], data['high'])
            & (data['open'] > data['low'])
            & (data['close'] > data['open'].shift(1))
        )

        return previous_candle & current_candle

    def bearish(self, data):
        previous_candle = (
            (data['close'].shift(1) > data['open'].shift(1))
            & (data['open'].shift(1) > data['low'].shift(1))
            & np.isclose(data['close'].shift(1), data['high'].shift(1))
        )

        current_candle = (
            (data['close'] < data['open'])
            & np.isclose(data['close'], data['low'])
            & (data['open'] < data['high'])
            & (data['close'] < data['open'].shift(1))
        )

        return previous_candle & current_candle
