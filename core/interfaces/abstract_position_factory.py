from abc import ABC, abstractmethod

from core.models.ohlcv import OHLCV
from core.models.position import Position
from core.models.signal import Signal


class AbstractPositionFactory(ABC):
    @abstractmethod
    def create_position(
        self,
        signal: Signal,
        ohlcv: OHLCV,
        entry_price: float,
        stop_loss: float | None,
    ) -> Position:
        pass
