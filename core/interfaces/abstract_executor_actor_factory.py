from abc import ABC, abstractmethod

from core.interfaces.abstract_market_repository import AbstractMarketRepository
from core.models.order import OrderType
from core.models.symbol import Symbol
from core.models.timeframe import Timeframe

from .abstract_actor import AbstractActor


class AbstractExecutorActorFactory(ABC):
    @abstractmethod
    def create_actor(
        self,
        type: OrderType,
        symbol: Symbol,
        timeframe: Timeframe,
        repository: AbstractMarketRepository,
    ) -> AbstractActor:
        pass
