import pandas as pd
from shared.meta_label import meta_label

from ta.patterns.abstract_pattern import AbstractPattern


@meta_label
class Piercing(AbstractPattern):
    NAME = 'PIERCING'

    @staticmethod
    def bullish(data):
        if len(data) < 2:
            return pd.Series(index=data.index, dtype=bool)

        first_candle = data.shift(1)
        second_candle = data

        long_bearish = first_candle['close'] < first_candle['open']
        long_bullish = second_candle['close'] > second_candle['open']
        close_above_midpoint = second_candle['close'] > (first_candle['open'] + first_candle['close']) / 2
        close_below_first_open = second_candle['close'] < first_candle['open']
        open_below_first_close = second_candle['open'] < first_candle['close']

        piercing = long_bearish & long_bullish & close_above_midpoint & close_below_first_open & open_below_first_close

        return piercing

    @staticmethod
    def bearish(data):
        if len(data) < 2:
            return pd.Series(index=data.index, dtype=bool)

        first_candle = data.shift(1)
        second_candle = data

        long_bullish = first_candle['close'] > first_candle['open']
        long_bearish = second_candle['close'] < second_candle['open']
        close_below_midpoint = second_candle['close'] < (first_candle['open'] + first_candle['close']) / 2
        close_above_first_open = second_candle['close'] > first_candle['open']
        open_above_first_close = second_candle['open'] > first_candle['close']

        dark_cloud_cover = long_bullish & long_bearish & close_below_midpoint & close_above_first_open & open_above_first_close

        return dark_cloud_cover
