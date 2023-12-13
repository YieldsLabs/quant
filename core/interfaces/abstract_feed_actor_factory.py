from abc import ABC, abstractmethod

from core.interfaces.abstract_actor import AbstractActor
from core.models.exchange import ExchangeType
from core.models.feed import FeedType
from core.models.strategy import Strategy
from core.models.symbol import Symbol
from core.models.timeframe import Timeframe


class AbstractFeedActorFactory(ABC):
    @abstractmethod
    def create_actor(
        self,
        feed_type: FeedType,
        symbol: Symbol,
        timeframe: Timeframe,
        strategy: Strategy,
        exchange_type: ExchangeType,
    ) -> AbstractActor:
        pass
