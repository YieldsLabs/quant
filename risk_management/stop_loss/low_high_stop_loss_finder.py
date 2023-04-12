from typing import Type

import numpy as np
from ohlcv.context import OhlcvContext
from risk_management.stop_loss.base.abstract_stop_loss_finder import AbstractStopLoss
from risk_management.stop_loss.atr_stop_loss_finder import ATRStopLossFinder
from shared.position_side import PositionSide


class LowHighStopLossFinder(AbstractStopLoss):
    NAME = 'LWHGH'

    def __init__(self, ohlcv: Type[OhlcvContext], atr_multi=1, lookback=50):
        super().__init__(ohlcv)
        self.stop_loss_finder = ATRStopLossFinder(ohlcv, atr_multi=atr_multi)
        self.lookback = lookback

    def next(self, position_side, entry_price):
        data = self.ohlcv_context.ohlcv

        if len(data) == 0:
            raise ValueError('Add ohlcv data')

        recent_data = data.tail(self.lookback)

        if position_side == PositionSide.LONG:
            low_series = recent_data['low']
            stop_loss_price = low_series[low_series < entry_price].min()
        elif position_side == PositionSide.SHORT:
            high_series = recent_data['high']
            stop_loss_price = high_series[high_series > entry_price].max()

        if np.isnan(stop_loss_price):
            return self.stop_loss_finder.next(position_side, entry_price)

        return stop_loss_price
