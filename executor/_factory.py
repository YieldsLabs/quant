from core.interfaces.abstract_actor import AbstractActor
from core.interfaces.abstract_executor_actor_factory import AbstractExecutorActorFactory
from core.interfaces.abstract_market_repository import AbstractMarketRepository
from core.models.order import OrderType
from core.models.symbol import Symbol
from core.models.timeframe import Timeframe

from ._market_actor import MarketOrderActor
from ._paper_actor import PaperOrderActor


class OrderExecutorActorFactory(AbstractExecutorActorFactory):
    _type = {
        OrderType.PAPER: PaperOrderActor,
        OrderType.MARKET: MarketOrderActor,
    }

    def __init__(self, repository: AbstractMarketRepository):
        super().__init__()
        self.repository = repository

    def create_actor(
        self,
        type: OrderType,
        symbol: Symbol,
        timeframe: Timeframe,
    ) -> AbstractActor:
        if type not in self._type:
            raise ValueError(f"Unknown OrderExecutor: {type}")

        order_cls = self._type.get(type)

        instance: AbstractActor = (
            order_cls(symbol, timeframe)
            if type == OrderType.MARKET
            else order_cls(symbol, timeframe, self.repository)
        )
        instance.start()
        return instance
