from abc import ABC, abstractmethod

from ..models.position import Position, PositionSide
from ..models.side import PositionSide
from ..models.strategy import Strategy

class AbstractPositionFactory(ABC):
    @abstractmethod
    def create_position(self, strategy: Strategy, position_side: PositionSide, account_size: float, entry_price: float, stop_loss_price: float | None) -> Position:
        pass
