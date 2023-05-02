from ta.patterns.abstract_pattern import AbstractPattern


class TweezerTopsBottoms(AbstractPattern):
    NAME = 'TWEEZER_TOPS_BOTTOMS'

    def bullish(self, data):
        is_first_bearish = data['close'].shift(1) < data['open'].shift(1)
        is_second_bullish = data['close'] > data['open']
        is_same_low = (data['low'].shift(1) - data['low']).abs() < ((data['high'].shift(1) - data['low'].shift(1)) * 0.1)

        return is_first_bearish & is_second_bullish & is_same_low

    def bearish(self, data):
        is_first_bullish = data['close'].shift(1) > data['open'].shift(1)
        is_second_bearish = data['close'] < data['open']
        is_same_high = (data['high'].shift(1) - data['high']).abs() < ((data['high'].shift(1) - data['low'].shift(1)) * 0.1)

        return is_first_bullish & is_second_bearish & is_same_high
