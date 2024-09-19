from abc import ABC, abstractmethod

from core.models.entity.position import Position
from core.models.entity.signal import Signal
from core.models.risk_type import SignalRiskType
from core.models.ta import TechAnalysis


class AbstractPositionFactory(ABC):
    @abstractmethod
    def create(
        self, signal: Signal, signal_risk_type: SignalRiskType, ta: TechAnalysis
    ) -> Position:
        pass
