from core.interfaces.abstract_signal_actor_factory import AbstractSignalActorFactory
from core.interfaces.abstract_signal_service import AbstractSignalService

from ._actor import SignalActor


class SignalActorFactory(AbstractSignalActorFactory):
    def __init__(self, service: AbstractSignalService):
        super().__init__()
        self.signal_service = service

    def create_actor(self, symbol, timeframe, strategy):
        actor = SignalActor(symbol, timeframe, strategy, self.signal_service)
        actor.start()
        return actor
