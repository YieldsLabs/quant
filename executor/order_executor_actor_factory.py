from core.interfaces.abstract_actor import AbstractActor
from core.interfaces.abstract_executor_actor_factory import AbstractExecutorActorFactory
from core.models.order import OrderType
from core.models.strategy import Strategy
from core.models.symbol import Symbol
from core.models.timeframe import Timeframe
from executor.paper_order_executor import PaperOrderExecutor

from .market_order_executor import MarketOrderExecutor


class OrderExecutorActorFactory(AbstractExecutorActorFactory):
    _order_type = {
        OrderType.PAPER: PaperOrderExecutor,
        OrderType.MARKET: MarketOrderExecutor,
    }

    def __init__(self):
        super().__init__()

    def create_actor(
        self,
        type: OrderType,
        symbol: Symbol,
        timeframe: Timeframe,
        strategy: Strategy,
    ) -> AbstractActor:
        if type not in self._order_type:
            raise ValueError(f"Unknown OrderExecutor: {type}")

        order_cls = self._order_type.get(type)

        return order_cls(symbol, timeframe, strategy)
