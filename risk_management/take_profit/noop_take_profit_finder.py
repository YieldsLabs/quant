from risk_management.take_profit.abstract_take_profit_finder import AbstractTakeProfit
from shared.meta_label import meta_label


@meta_label
class NoopTakeProfitFinder(AbstractTakeProfit):
    NAME = 'NOOP'

    def next(self, position_side, entry_price, stop_loss_price=0):
        return None

    def __str__(self):
        return f'{super().__str__()}'
