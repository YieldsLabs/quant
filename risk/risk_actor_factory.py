from core.interfaces.abstract_config import AbstractConfig
from core.interfaces.abstract_risk_actor_factory import AbstractRiskActorFactory
from core.models.strategy import Strategy
from core.models.symbol import Symbol
from core.models.timeframe import Timeframe

from .risk_actor import RiskActor


class RiskActorFactory(AbstractRiskActorFactory):
    def __init__(self, config_service: AbstractConfig):
        self.config = config_service.get('position')

    def create_actor(self, symbol: Symbol, timeframe: Timeframe, strategy: Strategy):
        return RiskActor(
            symbol,
            timeframe,
            strategy,
            self.config['risk_buffer'],
        )
