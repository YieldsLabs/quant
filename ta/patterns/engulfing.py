from ta.patterns.abstract_pattern import AbstractPattern


class Engulfing(AbstractPattern):
    NAME = 'ENGULFING'

    @staticmethod
    def bullish(data):
        return ((data['close'].shift(1) < data['open'].shift(1))
                & (data['close'] > data['open'])
                & (data['close'] > data['close'].shift(1))
                & (data['open'] < data['open'].shift(1)))

    @staticmethod
    def bearish(data):
        return ((data['close'].shift(1) > data['open'].shift(1))
                & (data['close'] < data['open'])
                & (data['close'] < data['close'].shift(1))
                & (data['open'] > data['open'].shift(1)))
