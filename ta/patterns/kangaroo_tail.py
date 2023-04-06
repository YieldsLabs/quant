class KangarooTail:
    @staticmethod
    def bullish(data, look_to_the_left=200):
        candle_range = data['high'] - data['low']
        two_third_candle_range = candle_range * 0.66

        bullish_kangaroo_tail = (
            (data['close'] > (two_third_candle_range + data['low']))
            & (data['open'] > (two_third_candle_range + data['low']))
            & (data['close'] > data['low'].shift(1))
            & (data['close'] < data['high'].shift(1))
            & (data['open'] > data['low'].shift(1))
            & (data['open'] < data['high'].shift(1))
            & (data['close'] < data['close'].shift(look_to_the_left))
            & (candle_range > candle_range.shift(1))
            & (candle_range > candle_range.shift(2))
            & (candle_range > candle_range.shift(3))
            & (data['close'].shift(1) < data['open'].shift(2))
            & (data['low'] <= data['low'].rolling(13).min())
        )
        return bullish_kangaroo_tail

    @staticmethod
    def bearish(data, look_to_the_left=200):
        candle_range = data['high'] - data['low']
        two_third_candle_range = candle_range * 0.66

        bearish_kangaroo_tail = (
            (data['close'] < (data['high'] - two_third_candle_range))
            & (data['open'] < (data['high'] - two_third_candle_range))
            & (data['close'] > data['low'].shift(1))
            & (data['close'] < data['high'].shift(1))
            & (data['open'] > data['low'].shift(1))
            & (data['open'] < data['high'].shift(1))
            & (data['close'] > data['close'].shift(look_to_the_left))
            & (candle_range > candle_range.shift(1))
            & (candle_range > candle_range.shift(2))
            & (candle_range > candle_range.shift(3))
            & (data['close'].shift(1) > data['open'].shift(1))
            & (data['high'] >= data['high'].rolling(13).max())
        )
        return bearish_kangaroo_tail

    def __str__(self) -> str:
        return '_KANGAROOTAIL'
