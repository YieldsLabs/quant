import numpy as np
from ta.patterns.abstract_pattern import AbstractPattern


class HaramiCross(AbstractPattern):
    NAME = 'HARAMICROSS'

    def bullish(self, data):
        is_previous_bearish = data['close'].shift(1) < data['open'].shift(1)
        is_current_doji = np.isclose(data['open'], data['close'])
        is_current_inside_previous = (data['open'] <= data['high'].shift(1)) & (data['close'] >= data['low'].shift(1))

        return is_previous_bearish & is_current_doji & is_current_inside_previous

    def bearish(self, data):
        is_previous_bullish = data['close'].shift(1) > data['open'].shift(1)
        is_current_doji = np.isclose(data['open'], data['close'])
        is_current_inside_previous = (data['open'] >= data['low'].shift(1)) & (data['close'] <= data['high'].shift(1))

        return is_previous_bullish & is_current_doji & is_current_inside_previous
