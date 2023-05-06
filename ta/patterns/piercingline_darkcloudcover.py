import pandas as pd

from .abstract_pattern import AbstractPattern


class PiercingLineDarkCloudCover(AbstractPattern):
    NAME = 'PIERCINGLINEDARKCLOUDCOVER'

    def bullish(self, data):
        first_candle = data.shift(1)
        second_candle = data

        long_bearish = first_candle['close'] < first_candle['open']
        long_bullish = second_candle['close'] > second_candle['open']
        close_above_midpoint = second_candle['close'] > (first_candle['open'] + first_candle['close']) / 2
        close_below_first_open = second_candle['close'] < first_candle['open']
        open_below_first_close = second_candle['open'] < first_candle['close']

        piercing = long_bearish & long_bullish & close_above_midpoint & close_below_first_open & open_below_first_close

        return piercing

    def bearish(self, data):
        first_candle = data.shift(1)
        second_candle = data

        long_bullish = first_candle['close'] > first_candle['open']
        long_bearish = second_candle['close'] < second_candle['open']
        close_below_midpoint = second_candle['close'] < (first_candle['open'] + first_candle['close']) / 2
        close_above_first_open = second_candle['close'] > first_candle['open']
        open_above_first_close = second_candle['open'] > first_candle['close']

        dark_cloud_cover = long_bullish & long_bearish & close_below_midpoint & close_above_first_open & open_above_first_close

        return dark_cloud_cover
