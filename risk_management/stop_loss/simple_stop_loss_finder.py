from risk_management.stop_loss.abstract_stop_loss_finder import AbstractStopLoss
from shared.trade_type import TradeType


class SimpleStopLossFinder(AbstractStopLoss):
    def __init__(self, stop_loss_pct=0.02):
        super().__init__()
        self.stop_loss_pct = stop_loss_pct

    def next(self, trade_type, entry_price):
        if trade_type.value == TradeType.LONG.value:
            stop_loss_price = entry_price * (1.0 - self.stop_loss_pct)
        elif trade_type.value == TradeType.SHORT.value:
            stop_loss_price = entry_price * (1.0 + self.stop_loss_pct)
        
        return stop_loss_price
    
    def reset(self):
        pass

    def set_ohlcv(self, data):
        pass
    
    def __str__(self) -> str:
        return f'SimpleStopLossFinder(stop_loss_pct={self.stop_loss_pct})'