from core.interfaces.abstract_config import AbstractConfig
from core.interfaces.abstract_exhange_factory import AbstractExchangeFactory
from core.interfaces.abstract_feed_actor_factory import AbstractFeedActorFactory
from core.models.exchange import ExchangeType
from core.models.feed import FeedType
from core.models.strategy import Strategy
from core.models.symbol import Symbol
from core.models.timeframe import Timeframe

from ._historical import HistoricalActor
from ._realtime import RealtimeActor


class FeedActorFactory(AbstractFeedActorFactory):
    def __init__(
        self,
        exchange_factory: AbstractExchangeFactory,
        ws_factory: AbstractExchangeFactory,
        config_service: AbstractConfig,
    ):
        self.config_service = config_service
        self.exchange_factory = exchange_factory
        self.ws_factory = ws_factory

    def create_actor(
        self,
        feed_type: FeedType,
        symbol: Symbol,
        timeframe: Timeframe,
        strategy: Strategy,
        exchange_type: ExchangeType,
    ):
        actor = (
            HistoricalActor(
                symbol,
                timeframe,
                strategy,
                self.exchange_factory.create(exchange_type),
                self.config_service,
            )
            if feed_type == FeedType.HISTORICAL
            else RealtimeActor(
                symbol,
                timeframe,
                strategy,
                self.ws_factory.create(exchange_type),
            )
        )
        actor.start()
        return actor
