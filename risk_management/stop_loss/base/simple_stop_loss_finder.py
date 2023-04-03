from typing import Type
from risk_management.stop_loss.base.abstract_stop_loss_finder import AbstractStopLoss
from shared.ohlcv_context import OhlcvContext
from shared.position_side import PositionSide


class SimpleStopLossFinder(AbstractStopLoss):
    def __init__(self, ohlcv: Type[OhlcvContext], stop_loss_pct=0.02):
        super().__init__(ohlcv)
        self.stop_loss_pct = stop_loss_pct

    def next(self, position_side, entry_price):
        if position_side == PositionSide.LONG:
            stop_loss_price = entry_price * (1.0 - self.stop_loss_pct)
        elif position_side == PositionSide.SHORT:
            stop_loss_price = entry_price * (1.0 + self.stop_loss_pct)
        
        return stop_loss_price
    
    def __str__(self) -> str:
        return f'SimpleStopLossFinder(stop_loss_pct={self.stop_loss_pct})'