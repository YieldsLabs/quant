from ta.patterns.abstract_pattern import AbstractPattern


class MorningEveningStar(AbstractPattern):
    NAME = 'MORNING_EVENING_STAR'

    def bullish(self, data):
        is_first_bearish = data['close'].shift(2) < data['open'].shift(2)
        is_second_small_body = (data['high'].shift(1) - data['low'].shift(1)) < (data['close'].shift(2) - data['open'].shift(2))
        is_third_bullish = data['close'] > data['open']
        is_gap_down = data['high'].shift(1) < data['low'].shift(2)
        is_gap_up = data['open'] < data['close'].shift(1)
        is_third_closes_above_first_midpoint = data['close'] > (data['open'].shift(2) + (data['close'].shift(2) - data['open'].shift(2)) / 2)

        return is_first_bearish & is_second_small_body & is_third_bullish & is_gap_down & is_gap_up & is_third_closes_above_first_midpoint

    def bearish(self, data):
        is_first_bullish = data['close'].shift(2) > data['open'].shift(2)
        is_second_small_body = (data['high'].shift(1) - data['low'].shift(1)) < (data['close'].shift(2) - data['open'].shift(2))
        is_third_bearish = data['close'] < data['open']
        is_gap_up = data['low'].shift(1) > data['high'].shift(2)
        is_gap_down = data['open'] > data['close'].shift(1)
        is_third_closes_below_first_midpoint = data['close'] < (data['open'].shift(2) + (data['close'].shift(2) - data['open'].shift(2)) / 2)

        return is_first_bullish & is_second_small_body & is_third_bearish & is_gap_up & is_gap_down & is_third_closes_below_first_midpoint
