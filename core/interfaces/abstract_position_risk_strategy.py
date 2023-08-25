from abc import ABC, abstractmethod

from ..models.side import PositionSide
from ..models.ohlcv import OHLCV

class AbstractPositionRiskStrategy(ABC):
    @abstractmethod
    def next(self, side: PositionSide, entry_price: float, stop_loss_price: float, ohlcv: OHLCV) -> float:
        pass