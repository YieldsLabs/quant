from ta.atr_indicator import ATRIndicator
from shared.trade_type import TradeType


class ATRStopLossFinder:
    def __init__(self, multiplier=1.5, atr_period=14):
        super().__init__()
        self.atr_indicator = ATRIndicator(atr_period)
        self.multiplier = multiplier
        self.data = []

    def set_ohlcv(self, data):
        self.data = data

    def reset(self):
        pass

    def next(self, entry_trade_type, entry_price):
        if len(self.data) == 0:
            raise ValueError('Add ohlcv data')
    
        atr_value = self.atr_indicator.atr(self.data)
        atr_value = atr_value.iloc[-1]

        if entry_trade_type.value == TradeType.LONG.value:
            stop_loss_price = entry_price - (atr_value * self.multiplier)
        
        elif entry_trade_type.value == TradeType.SHORT.value:
            stop_loss_price = entry_price + (atr_value * self.multiplier)


        return stop_loss_price
    
    def __str__(self) -> str:
        return f'ATRStopLossFinder(multiplier={self.multiplier}, atr_period={self.atr_indicator.period})'
