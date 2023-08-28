from abc import ABC, abstractmethod

from .abstract_actor import AbstractActor

from ..models.symbol import Symbol
from ..models.timeframe import Timeframe


class AbstractExecutorFactory(ABC):
    @abstractmethod
    def create_actor(self, symbol: Symbol, timeframe: Timeframe, live: bool) -> AbstractActor:
        pass
