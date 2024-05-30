from abc import ABC, abstractmethod

from core.models.strategy import Strategy
from core.models.strategy_ref import StrategyRef


class AbstractSignalService(ABC):
    @abstractmethod
    def register(self, strategy: Strategy) -> StrategyRef:
        pass
