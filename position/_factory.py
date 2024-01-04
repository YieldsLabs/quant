from core.interfaces.abstract_config import AbstractConfig
from core.interfaces.abstract_position_actor_factory import AbstractPositionActorFactory
from core.interfaces.abstract_position_factory import AbstractPositionFactory
from core.models.strategy import Strategy
from core.models.symbol import Symbol
from core.models.timeframe import Timeframe

from ._actor import PositionActor


class PositionActorFactory(AbstractPositionActorFactory):
    def __init__(
        self, position_factory: AbstractPositionFactory, config_service: AbstractConfig
    ):
        super().__init__()
        self.position_factory = position_factory
        self.config_service = config_service

    def create_actor(self, symbol: Symbol, timeframe: Timeframe, strategy: Strategy):
        actor = PositionActor(
            symbol, timeframe, strategy, self.position_factory, self.config_service
        )
        actor.start()
        return actor
