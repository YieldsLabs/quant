from ta.patterns.abstract_pattern import AbstractPattern


class Engulfing(AbstractPattern):
    NAME = 'ENGULFING'

    def bullish(self, data):
        return ((data['close'].shift(1) < data['open'].shift(1))
                & (data['close'] > data['open'])
                & (data['close'] > data['close'].shift(1))
                & (data['open'] < data['open'].shift(1)))

    def bearish(self, data):
        return ((data['close'].shift(1) > data['open'].shift(1))
                & (data['close'] < data['open'])
                & (data['close'] < data['close'].shift(1))
                & (data['open'] > data['open'].shift(1)))
