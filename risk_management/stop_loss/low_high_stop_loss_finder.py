from typing import Type
from risk_management.stop_loss.abstract_stop_loss_finder import AbstractStopLoss
from risk_management.stop_loss.simple_stop_loss_finder import SimpleStopLossFinder
from shared.ohlcv_context import OhlcvContext
from shared.trade_type import TradeType


class LowHighStopLossFinder(AbstractStopLoss):
    def __init__(self, ohlcv: Type[OhlcvContext], stop_loss_finder: Type[AbstractStopLoss], lookback_period=10):
        super().__init__(ohlcv)
        self.stop_loss_finder = stop_loss_finder
        self.lookback_period = lookback_period
        self.data = []


    def next(self, trade_type, entry_price=0):
        data = self.ohlcv_context.ohlcv

        if len(data) == 0:
            raise ValueError('Add ohlcv data')

        recent_data = data.tail(self.lookback_period)
        entry_price = recent_data['low'].min() if trade_type.value == TradeType.LONG.value else recent_data['high'].max()

        return self.stop_loss_finder.next(trade_type, entry_price)
    
    def __str__(self) -> str:
        return f'LowHighStopLossFinder(stop_loss_finder={self.stop_loss_finder}, lookback_period={self.lookback_period})'
