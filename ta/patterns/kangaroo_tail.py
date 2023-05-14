from .abstract_pattern import AbstractPattern


class KangarooTail(AbstractPattern):
    NAME = 'KANGAROOTAIL'

    def __init__(self, lookback=100):
        self.lookback = lookback

    def bullish(self, data):
        candle_range = data['high'] - data['low']
        two_third_candle_range = candle_range * 0.66
        lower_bound = two_third_candle_range + data['low']

        conditions = (
            (data['close'] > lower_bound)
            & (data['open'] > lower_bound)
            & (data['close'].between(data['low'].shift(1), data['high'].shift(1)))
            & (data['open'].between(data['low'].shift(1), data['high'].shift(1)))
            & (data['close'] < data['close'].shift(self.lookback))
            & (candle_range > candle_range.shift(1))
            & (candle_range > candle_range.shift(2))
            & (candle_range > candle_range.shift(3))
            & (data['close'].shift(1) < data['open'].shift(2))
            & (data['low'] <= data['low'].rolling(13).min())
        )

        return conditions

    def bearish(self, data):
        candle_range = data['high'] - data['low']
        two_third_candle_range = candle_range * 0.66
        upper_bound = data['high'] - two_third_candle_range

        conditions = (
            (data['close'] < upper_bound)
            & (data['open'] < upper_bound)
            & (data['close'].between(data['low'].shift(1), data['high'].shift(1)))
            & (data['open'].between(data['low'].shift(1), data['high'].shift(1)))
            & (data['close'] > data['close'].shift(self.lookback))
            & (candle_range > candle_range.shift(1))
            & (candle_range > candle_range.shift(2))
            & (candle_range > candle_range.shift(3))
            & (data['close'].shift(1) > data['open'].shift(1))
            & (data['high'] >= data['high'].rolling(13).max())
        )

        return conditions
