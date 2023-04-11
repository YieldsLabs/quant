from typing import Type

import numpy as np
from ohlcv.context import OhlcvContext
from risk_management.stop_loss.base.abstract_stop_loss_finder import AbstractStopLoss
from risk_management.stop_loss.base.simple_stop_loss_finder import SimpleStopLossFinder
from ta.volatility.atr import AverageTrueRange
from shared.position_side import PositionSide


class ATRStopLossFinder(AbstractStopLoss):
    NAME = 'ATR'

    def __init__(self, ohlcv: Type[OhlcvContext], period=14, atr_multi=1.5, stop_loss_pct=0.02):
        super().__init__(ohlcv)
        self.atr_indicator = AverageTrueRange(period)
        self.base_stop_loss_finder = SimpleStopLossFinder(ohlcv, stop_loss_pct=stop_loss_pct)
        self.atr_multi = atr_multi

    def next(self, position_side, entry_price):
        data = self.ohlcv_context.ohlcv

        if len(data) == 0:
            raise ValueError('Add ohlcv data')

        atr_value = self.atr_indicator.call(data)
        atr_value = atr_value.iloc[-1]

        if np.isnan(atr_value):
            return self.base_stop_loss_finder.next(position_side, entry_price)

        if position_side == PositionSide.LONG:
           return entry_price - (atr_value * self.atr_multi)

        if position_side == PositionSide.SHORT:
            return entry_price + (atr_value * self.atr_multi)
