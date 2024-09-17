from abc import ABC, abstractmethod
from typing import List, Tuple

from core.models.entity.ohlcv import OHLCV
from core.models.signal import SignalSide


class AbstractPositionRiskStrategy(ABC):
    @abstractmethod
    def next(
        self,
        side: SignalSide,
        entry_price: float,
        stop_loss_price: float,
        ohlcvs: List[Tuple[OHLCV]],
    ) -> float:
        pass
