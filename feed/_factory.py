from coral import DataSourceFactory
from core.interfaces.abstract_config import AbstractConfig
from core.interfaces.abstract_feed_actor_factory import AbstractFeedActorFactory
from core.models.datasource_type import DataSourceType
from core.models.feed import FeedType
from core.models.symbol import Symbol
from core.models.timeframe import Timeframe

from ._historical import HistoricalActor
from ._realtime import RealtimeActor


class FeedActorFactory(AbstractFeedActorFactory):
    def __init__(
        self,
        datasource_factory: DataSourceFactory,
        config_service: AbstractConfig,
    ):
        self.datasource_factory = datasource_factory
        self.config_service = config_service

    def create_actor(
        self,
        feed: FeedType,
        symbol: Symbol,
        timeframe: Timeframe,
        datasource: DataSourceType,
    ):
        actor = (
            HistoricalActor(
                symbol,
                timeframe,
                datasource,
                self.datasource_factory,
                self.config_service,
            )
            if feed == FeedType.HISTORICAL
            else RealtimeActor(
                symbol,
                timeframe,
                datasource,
                self.datasource_factory,
            )
        )
        actor.start()
        return actor
