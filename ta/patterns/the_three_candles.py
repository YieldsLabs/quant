from ta.patterns.abstract_pattern import AbstractPattern


class TheThreeCandles(AbstractPattern):
    NAME = 'THETHREECANDLES'

    @staticmethod
    def bullish(data):
        body = (data['close'] - data['open']).abs()
        condition = (data['close'] > data['close'].shift(1)) & \
                    (data['close'].shift(1) > data['close'].shift(2)) & \
                    (data['close'].shift(2) > data['close'].shift(3)) & \
                    (body >= body.rolling(window=5).max()) & \
                    (body.shift(1) >= body.shift(1).rolling(window=5).max()) & \
                    (body.shift(2) >= body.shift(2).rolling(window=5).max())
        return condition

    @staticmethod
    def bearish(data):
        body = (data['close'] - data['open']).abs()
        condition = (data['close'] < data['close'].shift(1)) & \
                    (data['close'].shift(1) < data['close'].shift(2)) & \
                    (data['close'].shift(2) < data['close'].shift(3)) & \
                    (body >= body.rolling(window=5).max()) & \
                    (body.shift(1) >= body.shift(1).rolling(window=5).max()) & \
                    (body.shift(2) >= body.shift(2).rolling(window=5).max())
        return condition
