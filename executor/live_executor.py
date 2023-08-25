from typing import Union
from core.commands.position import PositionClose

from core.interfaces.abstract_broker import AbstractBroker
from core.event_decorators import command_handler, event_handler
from core.events.position import PositionClosed, LongPositionOpened, ShortPositionOpened
from core.events.order import OrderFilled
from core.models.order import Order
from core.models.side import OrderSide
from core.interfaces.abstract_executor import AbstractExecutor


class LiveExecutor(AbstractExecutor):
    def __init__(self, broker: AbstractBroker):
        super().__init__()
        self.broker = broker

    @event_handler(LongPositionOpened)
    async def _on_long_position(self, event: LongPositionOpened):
        await self.execute_order(event)

    @event_handler(ShortPositionOpened)
    async def _on_short_position(self, event: ShortPositionOpened):
        await self.execute_order(event)

    @command_handler(PositionClose)
    async def _close_position(self, command: PositionClose):
        position = command.position

        self.broker.close_position(position.signal.symbol.name)

        await self.dispatcher.dispatch(PositionClosed(position))

    async def execute_order(self, event: Union[LongPositionOpened, ShortPositionOpened]):
        order_side = OrderSide.BUY if isinstance(event, LongPositionOpened) else OrderSide.SELL
        
        position = event.position
        symbol = position.signal.symbol.name

        current_order_id = self.broker.place_market_order(order_side, symbol, position.size)
        broker_position = self.broker.get_open_position(symbol)

        order = Order(id=current_order_id, side=order_side, size=broker_position['position_size'], price=broker_position['entry_price'])
        
        next_position = position.add_order(order).update_prices(order.price)
        
        await self.dispatcher.dispatch(OrderFilled(next_position))
