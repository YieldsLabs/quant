from abc import ABC, abstractmethod

from core.models.position import Position
from core.models.risk_type import SignalRiskType
from core.models.signal import Signal


class AbstractPositionFactory(ABC):
    @abstractmethod
    def create(self, signal: Signal, signal_risk_type: SignalRiskType) -> Position:
        pass
