from .abstract_pattern import AbstractPattern


class TheThreeCandles(AbstractPattern):
    NAME = 'THETHREECANDLES'

    def __init__(self, lookback=5):
        self.lookback = lookback

    def bullish(self, data):
        body = (data['close'] - data['open']).abs()
        condition = (data['close'] > data['close'].shift(1)) & \
                    (data['close'].shift(1) > data['close'].shift(2)) & \
                    (data['close'].shift(2) > data['close'].shift(3)) & \
                    (body >= body.rolling(window=self.lookback).max()) & \
                    (body.shift(1) >= body.shift(1).rolling(window=5).max()) & \
                    (body.shift(2) >= body.shift(2).rolling(window=5).max())
        return condition

    def bearish(self, data):
        body = (data['close'] - data['open']).abs()
        condition = (data['close'] < data['close'].shift(1)) & \
                    (data['close'].shift(1) < data['close'].shift(2)) & \
                    (data['close'].shift(2) < data['close'].shift(3)) & \
                    (body >= body.rolling(window=self.lookback).max()) & \
                    (body.shift(1) >= body.shift(1).rolling(window=5).max()) & \
                    (body.shift(2) >= body.shift(2).rolling(window=5).max())
        return condition
