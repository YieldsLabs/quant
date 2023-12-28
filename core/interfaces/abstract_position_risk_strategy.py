from abc import ABC, abstractmethod

from core.models.ohlcv import OHLCV
from core.models.signal import SignalSide


class AbstractPositionRiskStrategy(ABC):
    @abstractmethod
    def next(self, side: SignalSide, stop_loss_price: float, ohlcv: OHLCV) -> float:
        pass
