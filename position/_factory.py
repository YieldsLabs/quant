from core.interfaces.abstract_position_actor_factory import AbstractPositionActorFactory
from core.models.symbol import Symbol
from core.models.timeframe import Timeframe

from ._actor import PositionActor


class PositionActorFactory(AbstractPositionActorFactory):
    def __init__(self):
        super().__init__()

    def create_actor(self, symbol: Symbol, timeframe: Timeframe):
        actor = PositionActor(symbol, timeframe)
        actor.start()
        return actor
