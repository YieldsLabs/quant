from ta.patterns.abstract_pattern import AbstractPattern


class Harami(AbstractPattern):
    NAME = 'HARAMI'

    @staticmethod
    def bullish(data):
        previous_row = data.iloc[-2]
        current_row = data.iloc[-1]

        is_previous_bearish = previous_row['close'] < previous_row['open']
        is_current_bullish = current_row['close'] > current_row['open']
        is_current_inside_previous = current_row['open'] <= previous_row['high'] and current_row['close'] >= previous_row['low']
        is_previous_long = previous_row['high'] - previous_row['low'] > previous_row['close'] - previous_row['open']

        return is_previous_bearish and is_current_bullish and is_current_inside_previous and is_previous_long

    @staticmethod
    def bearish(data):
        previous_row = data.iloc[-2]
        current_row = data.iloc[-1]

        is_previous_bullish = previous_row['close'] > previous_row['open']
        is_current_bearish = current_row['close'] < current_row['open']
        is_current_inside_previous = current_row['open'] >= previous_row['low'] and current_row['close'] <= previous_row['high']
        is_previous_long = previous_row['high'] - previous_row['low'] > previous_row['close'] - previous_row['open']

        return is_previous_bullish and is_current_bearish and is_current_inside_previous and is_previous_long
