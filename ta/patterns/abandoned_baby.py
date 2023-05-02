from ta.patterns.abstract_pattern import AbstractPattern


class AbandonedBaby(AbstractPattern):
    NAME = 'ABANDONED_BABY'

    def bullish(self, data):
        is_first_bearish = data['close'].shift(2) < data['open'].shift(2)
        is_doji = (data['open'].shift(1) - data['close'].shift(1)).abs() < ((data['high'].shift(1) - data['low'].shift(1)) * 0.1)
        is_third_bullish = data['close'] > data['open']
        is_gap_down = data['high'].shift(1) < data['low'].shift(2)
        is_gap_up = data['low'] > data['high'].shift(1)

        return is_first_bearish & is_doji & is_third_bullish & is_gap_down & is_gap_up

    def bearish(self, data):
        is_first_bullish = data['close'].shift(2) > data['open'].shift(2)
        is_doji = (data['open'].shift(1) - data['close'].shift(1)).abs() < ((data['high'].shift(1) - data['low'].shift(1)) * 0.1)
        is_third_bearish = data['close'] < data['open']
        is_gap_up = data['low'].shift(1) > data['high'].shift(2)
        is_gap_down = data['high'] < data['low'].shift(1)

        return is_first_bullish & is_doji & is_third_bearish & is_gap_up & is_gap_down
