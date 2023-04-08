from abc import ABC, abstractmethod

from shared.position_side import PositionSide


class AbstractTakeProfit(ABC):
    SUFFIX = "_TAKEPROFIT"
    NAME = ""

    @abstractmethod
    def next(self, position_side: PositionSide, entry_price: float, stop_loss_price: float):
        pass

    def __str__(self) -> str:
        return f'{self.SUFFIX}{self.NAME}'
