from typing import Type
from ohlcv.context import OhlcvContext
from risk_management.stop_loss.base.abstract_stop_loss_finder import AbstractStopLoss
from risk_management.stop_loss.base.atr_stop_loss_finder import ATRStopLossFinder
from shared.position_side import PositionSide


class LowHighStopLossFinder(AbstractStopLoss):
    NAME = 'LOWHIGH'

    def __init__(self, ohlcv: Type[OhlcvContext], atr_multi=1, lookback=10):
        super().__init__(ohlcv)
        self.stop_loss_finder = ATRStopLossFinder(ohlcv, atr_multi=atr_multi)
        self.lookback = lookback

    def next(self, position_side, entry_price=0):
        data = self.ohlcv_context.ohlcv

        if len(data) == 0:
            raise ValueError('Add ohlcv data')

        recent_data = data.tail(self.lookback)
        entry_price = recent_data['low'].min() if position_side == PositionSide.LONG else recent_data['high'].max()

        return self.stop_loss_finder.next(position_side, entry_price)
