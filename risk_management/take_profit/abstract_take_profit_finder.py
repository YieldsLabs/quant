from abc import ABC, abstractmethod

from shared.trade_type import TradeType


class AbstractTakeProfit(ABC):
    @abstractmethod
    def next(self, trade_type: TradeType, entry_price: float, stop_loss_price: float):
        pass