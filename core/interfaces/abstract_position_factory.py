from abc import ABC, abstractmethod

from ..models.signal import Signal
from ..models.position import Position

class AbstractPositionFactory(ABC):
    @abstractmethod
    def create_position(self, signal: Signal, account_size: float, entry_price: float, stop_loss: float | None) -> Position:
        pass
