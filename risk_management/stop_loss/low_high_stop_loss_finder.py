import numpy as np
import pandas as pd
from risk_management.stop_loss.base.abstract_stop_loss_finder import AbstractStopLoss
from risk_management.stop_loss.atr_stop_loss_finder import ATRStopLossFinder


class LowHighStopLossFinder(AbstractStopLoss):
    NAME = 'LWHGH'

    def __init__(self, atr_multi=0.87, lookback=50):
        super().__init__()
        self.stop_loss_finder = ATRStopLossFinder(atr_multi=atr_multi)
        self.lookback = lookback

    def next(self, entry, ohlcv):
        if len(ohlcv) == 0:
            raise ValueError('Add ohlcv data')

        recent_data = ohlcv.tail(self.lookback)
        high_series, low_series = recent_data['high'], recent_data['low']

        long_stop_loss_price = low_series[low_series < entry].min()
        short_stop_loss_price = high_series[high_series > entry].max()

        if np.isnan(long_stop_loss_price) or np.isnan(short_stop_loss_price):
            return self.stop_loss_finder.next(entry, ohlcv)

        return long_stop_loss_price, short_stop_loss_price
