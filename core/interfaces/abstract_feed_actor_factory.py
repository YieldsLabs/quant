from abc import ABC, abstractmethod

from core.interfaces.abstract_actor import AbstractActor
from core.models.datasource_type import DataSourceType
from core.models.feed import FeedType
from core.models.symbol import Symbol
from core.models.timeframe import Timeframe


class AbstractFeedActorFactory(ABC):
    @abstractmethod
    def create_actor(
        self,
        feed: FeedType,
        symbol: Symbol,
        timeframe: Timeframe,
        datasource: DataSourceType,
    ) -> AbstractActor:
        pass
