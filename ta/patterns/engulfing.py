from .abstract_pattern import AbstractPattern


class Engulfing(AbstractPattern):
    NAME = 'ENGULFING'

    def bullish(self, data):
        previous_candle_bearish = data['close'].shift(1) < data['open'].shift(1)
        current_candle_bullish = data['close'] > data['open']
        close_greater_than_previous = data['close'] > data['close'].shift(1)
        open_less_than_previous = data['open'] < data['open'].shift(1)

        return previous_candle_bearish & current_candle_bullish & close_greater_than_previous & open_less_than_previous

    def bearish(self, data):
        previous_candle_bullish = data['close'].shift(1) > data['open'].shift(1)
        current_candle_bearish = data['close'] < data['open']
        close_less_than_previous = data['close'] < data['close'].shift(1)
        open_greater_than_previous = data['open'] > data['open'].shift(1)

        return previous_candle_bullish & current_candle_bearish & close_less_than_previous & open_greater_than_previous
