import numpy as np


class SplitCandlestickPattern:
    @staticmethod
    def bullish(data):
        bullish_split = (
            (data['close'].shift(1) < data['open'].shift(1)) &
            (data['open'].shift(1) < data['high'].shift(1)) &
            np.isclose(data['close'].shift(1), data['low'].shift(1)) &
            (data['close'] > data['open']) &
            np.isclose(data['close'], data['high']) &
            (data['open'] > data['low']) &
            (data['close'] > data['open'].shift(1))
        )

        return bullish_split

    @staticmethod
    def bearish(data):
        bearish_split = (
            (data['close'].shift(1) > data['open'].shift(1)) &
            (data['open'].shift(1) > data['low'].shift(1)) &
            np.isclose(data['close'].shift(1), data['high'].shift(1)) &
            (data['close'] < data['open']) &
            np.isclose(data['close'], data['low']) &
            (data['open'] < data['high']) &
            (data['close'] < data['open'].shift(1))
        )

        return bearish_split
