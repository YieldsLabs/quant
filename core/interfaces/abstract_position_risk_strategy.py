from abc import ABC, abstractmethod
from typing import List

from core.models.ohlcv import OHLCV
from core.models.signal import SignalSide


class AbstractPositionRiskStrategy(ABC):
    @abstractmethod
    def next(
        self, side: SignalSide, entry_price: float, stop_loss_price: float, ohlcvs: List[OHLCV]
    ) -> float:
        pass
