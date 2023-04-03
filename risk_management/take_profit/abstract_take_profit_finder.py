from abc import ABC, abstractmethod

from shared.position_side import PositionSide


class AbstractTakeProfit(ABC):
    @abstractmethod
    def next(self, position_side: PositionSide, entry_price: float, stop_loss_price: float):
        pass