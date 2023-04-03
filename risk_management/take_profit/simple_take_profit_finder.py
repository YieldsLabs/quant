from risk_management.take_profit.abstract_take_profit_finder import AbstractTakeProfit
from shared.position_side import PositionSide


class SimpleTakeProfitFinder(AbstractTakeProfit):
    def __init__(self, take_profit_pct=0.03):
        super().__init__()
        self.take_profit_pct = take_profit_pct

    def next(self, position_side, entry_price, stop_loss_price=0.0):
        if position_side == PositionSide.LONG :
            take_profit_price = entry_price * (1.0 + self.take_profit_pct)
        elif position_side == PositionSide.SHORT :
            take_profit_price = entry_price * (1.0 - self.take_profit_pct)
        
        return take_profit_price
    
    def __str__(self) -> str:
        return f'SimpleTakeProfitFinder(take_profit_pct={self.take_profit_pct})'
    