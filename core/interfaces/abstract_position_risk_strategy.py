from abc import ABC, abstractmethod

from ..models.signal import SignalSide
from ..models.ohlcv import OHLCV


class AbstractPositionRiskStrategy(ABC):
    @abstractmethod
    def next(self, side: SignalSide, entry_price: float, stop_loss_price: float, ohlcv: OHLCV) -> float:
        pass