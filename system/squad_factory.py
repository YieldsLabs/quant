from core.interfaces.abstract_executor_actor_factory import AbstractExecutorActorFactory
from core.interfaces.abstract_position_actor_factory import AbstractPositionActorFactory
from core.interfaces.abstract_risk_actor_factory import AbstractRiskActorFactory
from core.interfaces.abstract_signal_actor_factory import AbstractSignalActorFactory
from core.interfaces.abstract_squad_factory import AbstractSquadFactory

from .squad import Squad


class SquadFactory(AbstractSquadFactory):
    def __init__(
        self,
        signal_factory: AbstractSignalActorFactory,
        executor_factory: AbstractExecutorActorFactory,
        position_factory: AbstractPositionActorFactory,
        risk_factory: AbstractRiskActorFactory,
    ):
        super().__init__()

        self.signal_factory = signal_factory
        self.executor_factory = executor_factory
        self.position_factory = position_factory
        self.risk_factory = risk_factory

    def create_squad(self, symbol, timeframe, strategy):
        signal_actor = self.signal_factory.create_actor(symbol, timeframe, strategy)
        executor_actor = self.executor_factory.create_actor(symbol, timeframe, strategy)
        position_actor = self.position_factory.create_actor(symbol, timeframe, strategy)
        risk_actor = self.risk_factory.create_actor(symbol, timeframe, strategy)

        return Squad(signal_actor, position_actor, risk_actor, executor_actor)
