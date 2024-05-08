from core.interfaces.abstract_config import AbstractConfig
from core.interfaces.abstract_market_repository import AbstractMarketRepository
from core.interfaces.abstract_risk_actor_factory import AbstractRiskActorFactory
from core.models.symbol import Symbol
from core.models.timeframe import Timeframe

from ._actor import RiskActor


class RiskActorFactory(AbstractRiskActorFactory):
    def __init__(
        self, config_service: AbstractConfig, repository: AbstractMarketRepository
    ):
        self.config_service = config_service
        self.repository = repository

    def create_actor(self, symbol: Symbol, timeframe: Timeframe):
        actor = RiskActor(
            symbol,
            timeframe,
            self.config_service,
            self.repository,
        )
        actor.start()
        return actor
