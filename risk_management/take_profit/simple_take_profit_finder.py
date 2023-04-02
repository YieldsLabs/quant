from risk_management.take_profit.abstract_take_profit_finder import AbstractTakeProfit
from shared.trade_type import TradeType


class SimpleTakeProfitFinder(AbstractTakeProfit):
    def __init__(self, take_profit_pct=0.03):
        super().__init__()
        self.take_profit_pct = take_profit_pct

    def next(self, trade_type, entry_price, stop_loss_price=0.0):
        if trade_type.value == TradeType.LONG.value :
            take_profit_price = entry_price * (1.0 + self.take_profit_pct)
        elif trade_type.value == TradeType.SHORT.value :
            take_profit_price = entry_price * (1.0 - self.take_profit_pct)
        
        return take_profit_price
    
    def __str__(self) -> str:
        return f'SimpleTakeProfitFinder(take_profit_pct={self.take_profit_pct})'
    