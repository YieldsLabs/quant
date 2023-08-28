from core.interfaces.abstract_position_actor_factory import AbstractPositionActorFactory
from core.interfaces.abstract_position_factory import AbstractPositionFactory
from core.models.symbol import Symbol
from core.models.timeframe import Timeframe

from .position_actor import PositionActor


class PositionActorFactory(AbstractPositionActorFactory):
    def __init__(self, position_factory: AbstractPositionFactory):
        super().__init__()
        self.position_factory = position_factory
    
    def create_actor(self, symbol: Symbol, timeframe: Timeframe, account_size: int = 1000):
        return PositionActor(
            symbol,
            timeframe,
            self.position_factory,
            account_size
        )
        
