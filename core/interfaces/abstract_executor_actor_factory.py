from abc import ABC, abstractmethod

from .abstract_actor import AbstractActor

from ..models.strategy import Strategy
from ..models.symbol import Symbol
from ..models.timeframe import Timeframe


class AbstractExecutorActorFactory(ABC):
    @abstractmethod
    def create_actor(self, symbol: Symbol, timeframe: Timeframe, strategy: Strategy, live: bool) -> AbstractActor:
        pass
