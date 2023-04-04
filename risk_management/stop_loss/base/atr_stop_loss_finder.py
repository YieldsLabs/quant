from typing import Type
from ohlcv.context import OhlcvContext
from risk_management.stop_loss.base.abstract_stop_loss_finder import AbstractStopLoss
from ta.indicators.atr_indicator import ATRIndicator
from shared.position_side import PositionSide


class ATRStopLossFinder(AbstractStopLoss):
    def __init__(self, ohlcv: Type[OhlcvContext], multiplier=1.5, atr_period=14):
        super().__init__(ohlcv)
        self.atr_indicator = ATRIndicator(atr_period)
        self.multiplier = multiplier

    def next(self, position_side, entry_price):
        data = self.ohlcv_context.ohlcv

        if len(data) == 0:
            raise ValueError('Add ohlcv data')

        atr_value = self.atr_indicator.call(data)
        atr_value = atr_value.iloc[-1]

        if position_side == PositionSide.LONG:
            stop_loss_price = entry_price - (atr_value * self.multiplier)

        elif position_side == PositionSide.SHORT:
            stop_loss_price = entry_price + (atr_value * self.multiplier)

        return stop_loss_price

    def __str__(self) -> str:
        return f'ATRStopLossFinder(multiplier={self.multiplier}, atr={self.atr_indicator})'
