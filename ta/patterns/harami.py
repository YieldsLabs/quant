from ta.patterns.abstract_pattern import AbstractPattern


class Harami(AbstractPattern):
    NAME = 'HARAMI'

    @staticmethod
    def bullish(data):
        is_previous_bearish = data['close'].shift(1) < data['open'].shift(1)
        is_current_bullish = data['close'] > data['open']
        is_current_inside_previous = (data['open'] <= data['high'].shift(1)) & (data['close'] >= data['low'].shift(1))
        is_previous_long = (data['high'].shift(1) - data['low'].shift(1)) > (data['close'].shift(1) - data['open'].shift(1))

        return is_previous_bearish & is_current_bullish & is_current_inside_previous & is_previous_long

    @staticmethod
    def bearish(data):
        is_previous_bullish = data['close'].shift(1) > data['open'].shift(1)
        is_current_bearish = data['close'] < data['open']
        is_current_inside_previous = (data['open'] >= data['low'].shift(1)) & (data['close'] <= data['high'].shift(1))
        is_previous_long = (data['high'].shift(1) - data['low'].shift(1)) > (data['close'].shift(1) - data['open'].shift(1))

        return is_previous_bullish & is_current_bearish & is_current_inside_previous & is_previous_long
