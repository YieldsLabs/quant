from .abstract_pattern import AbstractPattern


class KangarooTail(AbstractPattern):
    NAME = 'KANGAROOTAIL'

    def __init__(self, lookback=200):
        self.lookback = lookback

    def bullish(self, data):
        candle_range = data['high'] - data['low']
        two_third_candle_range = candle_range * 0.66

        return (
            (data['close'] > (two_third_candle_range + data['low']))
            & (data['open'] > (two_third_candle_range + data['low']))
            & (data['close'] > data['low'].shift(1))
            & (data['close'] < data['high'].shift(1))
            & (data['open'] > data['low'].shift(1))
            & (data['open'] < data['high'].shift(1))
            & (data['close'] < data['close'].shift(self.lookback))
            & (candle_range > candle_range.shift(1))
            & (candle_range > candle_range.shift(2))
            & (candle_range > candle_range.shift(3))
            & (data['close'].shift(1) < data['open'].shift(2))
            & (data['low'] <= data['low'].rolling(13).min())
        )

    def bearish(self, data):
        candle_range = data['high'] - data['low']
        two_third_candle_range = candle_range * 0.66

        return (
            (data['close'] < (data['high'] - two_third_candle_range))
            & (data['open'] < (data['high'] - two_third_candle_range))
            & (data['close'] > data['low'].shift(1))
            & (data['close'] < data['high'].shift(1))
            & (data['open'] > data['low'].shift(1))
            & (data['open'] < data['high'].shift(1))
            & (data['close'] > data['close'].shift(self.lookback))
            & (candle_range > candle_range.shift(1))
            & (candle_range > candle_range.shift(2))
            & (candle_range > candle_range.shift(3))
            & (data['close'].shift(1) > data['open'].shift(1))
            & (data['high'] >= data['high'].rolling(13).max())
        )
