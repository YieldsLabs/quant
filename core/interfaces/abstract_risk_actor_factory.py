from abc import ABC, abstractmethod

from core.models.symbol import Symbol
from core.models.timeframe import Timeframe

from .abstract_actor import AbstractActor


class AbstractRiskActorFactory(ABC):
    @abstractmethod
    def create_actor(self, symbol: Symbol, timeframe: Timeframe) -> AbstractActor:
        pass
