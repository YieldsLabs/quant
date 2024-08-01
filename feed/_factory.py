from core.interfaces.abstract_config import AbstractConfig
from core.interfaces.abstract_exhange_factory import AbstractExchangeFactory
from core.interfaces.abstract_feed_actor_factory import AbstractFeedActorFactory
from core.interfaces.abstract_timeseries import AbstractTimeSeriesService
from core.models.exchange import ExchangeType
from core.models.feed import FeedType
from core.models.symbol import Symbol
from core.models.timeframe import Timeframe

from ._historical import HistoricalActor
from ._realtime import RealtimeActor


class FeedActorFactory(AbstractFeedActorFactory):
    def __init__(
        self,
        exchange_factory: AbstractExchangeFactory,
        ws_factory: AbstractExchangeFactory,
        ts_service: AbstractTimeSeriesService,
        config_service: AbstractConfig,
    ):
        self.config_service = config_service
        self.exchange_factory = exchange_factory
        self.ws_factory = ws_factory
        self.ts_service = ts_service

    def create_actor(
        self,
        feed_type: FeedType,
        symbol: Symbol,
        timeframe: Timeframe,
        exchange_type: ExchangeType,
    ):
        actor = (
            HistoricalActor(
                symbol,
                timeframe,
                self.exchange_factory.create(exchange_type),
                self.ts_service,
                self.config_service,
            )
            if feed_type == FeedType.HISTORICAL
            else RealtimeActor(
                symbol,
                timeframe,
                self.ws_factory.create(exchange_type),
                self.ts_service,
            )
        )
        actor.start()
        return actor
