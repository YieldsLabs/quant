from risk_management.take_profit.abstract_take_profit_finder import AbstractTakeProfit


class NoopTakeProfitFinder(AbstractTakeProfit):
    def next(self, trade_type, entry_price, stop_loss_price=0):
        return None
    
    def __str__(self) -> str:
        return f'NoopTakeProfitFinder()'
    
