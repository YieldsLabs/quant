from typing import Type
from ohlcv.context import OhlcvContext
from risk_management.stop_loss.base.abstract_stop_loss_finder import AbstractStopLoss
from ta.volatility.atr import AverageTrueRange
from shared.position_side import PositionSide


class ATRStopLossFinder(AbstractStopLoss):
    NAME = 'ATR'

    def __init__(self, ohlcv: Type[OhlcvContext], period=14, atr_multi=1.5):
        super().__init__(ohlcv)
        self.atr_indicator = AverageTrueRange(period)
        self.atr_multi = atr_multi

    def next(self, position_side, entry_price):
        data = self.ohlcv_context.ohlcv

        if len(data) == 0:
            raise ValueError('Add ohlcv data')

        atr_value = self.atr_indicator.call(data)
        atr_value = atr_value.iloc[-1]

        if position_side == PositionSide.LONG:
            stop_loss_price = entry_price - (atr_value * self.atr_multi)

        elif position_side == PositionSide.SHORT:
            stop_loss_price = entry_price + (atr_value * self.atr_multi)

        return stop_loss_price
