from abc import ABC, abstractmethod

from ..models.ohlcv import OHLCV
from ..models.signal import Signal
from ..models.position import Position


class AbstractPositionFactory(ABC):
    @abstractmethod
    def create_position(self, signal: Signal, ohlcv: OHLCV, account_size: float, entry_price: float, stop_loss: float | None) -> Position:
        pass
