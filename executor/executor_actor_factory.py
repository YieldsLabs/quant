from core.interfaces.abstract_actor import AbstractActor
from core.interfaces.abstract_executor_actor_factory import AbstractExecutorActorFactory
from core.models.strategy import Strategy
from core.models.symbol import Symbol
from core.models.timeframe import Timeframe

from .live_executor import LiveExecutor
from .paper_executor import PaperExecutor


class ExecutorActorFactory(AbstractExecutorActorFactory):
    def __init__(self, slippage: float):
        super().__init__()
        self.slippage = slippage

    def create_actor(
        self,
        symbol: Symbol,
        timeframe: Timeframe,
        strategy: Strategy,
        live: bool = False,
    ) -> AbstractActor:
        if live:
            return LiveExecutor(symbol, timeframe, strategy)
        else:
            return PaperExecutor(symbol, timeframe, strategy, self.slippage)
