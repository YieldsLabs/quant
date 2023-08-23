from typing import Type, Union

from core.interfaces.abstract_broker import AbstractBroker
from core.event_decorators import event_handler
from core.events.position import PositionClosed, LongPositionOpened, ShortPositionOpened, OrderFilled
from core.models.order import Order, OrderSide
from core.interfaces.abstract_executor import AbstractExecutor


class LiveExecutor(AbstractExecutor):
    def __init__(self, broker: Type[AbstractBroker]):
        super().__init__()
        self.broker = broker

    @event_handler(LongPositionOpened)
    async def _on_long_position(self, event: LongPositionOpened):
        await self.execute_order(event)

    @event_handler(ShortPositionOpened)
    async def _on_short_position(self, event: ShortPositionOpened):
        await self.execute_order(event)

    @event_handler(PositionClosed)
    async def _on_close_position(self, event: PositionClosed):
        self.broker.close_position(event.strategy.symbol)

    async def execute_order(self, event: Union[LongPositionOpened, ShortPositionOpened]):
        order_side = OrderSide.BUY if isinstance(event, LongPositionOpened) else OrderSide.SELL
        strategy = event.strategy
        symbol = strategy.symbol

        current_order_id = self.broker.place_market_order(order_side, symbol, event.size)
        position = self.broker.get_open_position(symbol)

        order = Order(id=current_order_id, side=order_side, size=position['position_size'], price=position['entry_price'])

        await self.dispatcher.dispatch(
            OrderFilled(strategy=strategy, order=order))
