from typing import Type
from ohlcv.context import OhlcvContext
from risk_management.stop_loss.base.abstract_stop_loss_finder import AbstractStopLoss
from shared.meta_label import meta_label
from shared.position_side import PositionSide


@meta_label
class LowHighStopLossFinder(AbstractStopLoss):
    NAME = 'LOWHIGH'

    def __init__(self, ohlcv: Type[OhlcvContext], stop_loss_finder: Type[AbstractStopLoss], lookback=10):
        super().__init__(ohlcv)
        self.stop_loss_finder = stop_loss_finder
        self.lookback = lookback

    def next(self, position_side, entry_price=0):
        data = self.ohlcv_context.ohlcv

        if len(data) == 0:
            raise ValueError('Add ohlcv data')

        recent_data = data.tail(self.lookback)
        entry_price = recent_data['low'].min() if position_side == PositionSide.LONG else recent_data['high'].max()

        return self.stop_loss_finder.next(position_side, entry_price)
