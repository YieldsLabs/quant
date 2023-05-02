from .abstract_pattern import AbstractPattern


class ThreeWhiteSoldiersThreeBlackCrows(AbstractPattern):
    NAME = 'THREEWHITESOLDIERSTHREEBLACKCROWS'

    def __init__(self, lookback=5):
        self.lookback = lookback

    def bullish(self, data):
        body = (data['close'] - data['open']).abs()
        consecutive_increases = (
            (data['close'] > data['close'].shift(1))
            & (data['close'].shift(1) > data['close'].shift(2))
            & (data['close'].shift(2) > data['close'].shift(3))
        )
        large_bodies = (
            (body >= body.rolling(window=self.lookback).max())
            & (body.shift(1) >= body.shift(1).rolling(window=self.lookback).max())
            & (body.shift(2) >= body.shift(2).rolling(window=self.lookback).max())
        )

        return consecutive_increases & large_bodies

    def bearish(self, data):
        body = (data['close'] - data['open']).abs()
        consecutive_decreases = (
            (data['close'] < data['close'].shift(1))
            & (data['close'].shift(1) < data['close'].shift(2))
            & (data['close'].shift(2) < data['close'].shift(3))
        )
        large_bodies = (
            (body >= body.rolling(window=self.lookback).max())
            & (body.shift(1) >= body.shift(1).rolling(window=self.lookback).max())
            & (body.shift(2) >= body.shift(2).rolling(window=self.lookback).max())
        )

        return consecutive_decreases & large_bodies
