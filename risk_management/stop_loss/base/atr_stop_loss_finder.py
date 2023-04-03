from typing import Type
from risk_management.stop_loss.base.abstract_stop_loss_finder import AbstractStopLoss
from shared.ohlcv_context import OhlcvContext
from ta.atr_indicator import ATRIndicator
from shared.trade_type import TradeType


class ATRStopLossFinder(AbstractStopLoss):
    def __init__(self, ohlcv: Type[OhlcvContext], multiplier=1.5, atr_period=14):
        super().__init__(ohlcv)
        self.atr_indicator = ATRIndicator(atr_period)
        self.multiplier = multiplier

    def next(self, entry_trade_type, entry_price):
        data = self.ohlcv_context.ohlcv

        if len(data) == 0:
            raise ValueError('Add ohlcv data')
    
        atr_value = self.atr_indicator.atr(data)
        atr_value = atr_value.iloc[-1]

        if entry_trade_type.value == TradeType.LONG.value:
            stop_loss_price = entry_price - (atr_value * self.multiplier)
        
        elif entry_trade_type.value == TradeType.SHORT.value:
            stop_loss_price = entry_price + (atr_value * self.multiplier)


        return stop_loss_price
    
    def reset(self):
        pass
    
    def __str__(self) -> str:
        return f'ATRStopLossFinder(multiplier={self.multiplier}, atr_period={self.atr_indicator.period})'
