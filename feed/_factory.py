from coral import DataSourceFactory
from core.interfaces.abstract_config import AbstractConfig
from core.interfaces.abstract_feed_actor_factory import AbstractFeedActorFactory
from core.models.feed import FeedType
from core.models.symbol import Symbol
from core.models.timeframe import Timeframe

from ._historical import HistoricalActor
from ._realtime import RealtimeActor


class FeedActorFactory(AbstractFeedActorFactory):
    def __init__(
        self,
        datasource: DataSourceFactory,
        config_service: AbstractConfig,
    ):
        self.datasource = datasource
        self.config_service = config_service

    def create_actor(
        self,
        feed_type: FeedType,
        symbol: Symbol,
        timeframe: Timeframe,
    ):
        actor = (
            HistoricalActor(
                symbol,
                timeframe,
                self.datasource,
                self.config_service,
            )
            if feed_type == FeedType.HISTORICAL
            else RealtimeActor(
                symbol,
                timeframe,
                self.datasource,
            )
        )
        actor.start()
        return actor
