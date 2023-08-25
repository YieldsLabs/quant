import asyncio
from typing import Union
from core.commands.position import PositionClose

from core.event_decorators import command_handler, event_handler
from core.events.position import LongPositionOpened, PositionClosed, ShortPositionOpened
from core.events.order import OrderFilled
from core.models.order import Order
from core.models.side import OrderSide
from core.interfaces.abstract_executor import AbstractExecutor


class PaperExecutor(AbstractExecutor):
    def __init__(self, slippage: float):
        super().__init__()
        self.slippage = slippage

    @command_handler(PositionClose)
    async def _close_position(self, command: PositionClose):
        await self.dispatcher.dispatch(PositionClosed(command.position))

    @event_handler(LongPositionOpened)
    async def _on_long_position(self, event: LongPositionOpened):
        await self.execute_order(event)

    @event_handler(ShortPositionOpened)
    async def _on_short_position(self, event: ShortPositionOpened):
        await self.execute_order(event)

    async def execute_order(self, event: Union[LongPositionOpened, ShortPositionOpened]):
        position = event.position

        order_side = OrderSide.BUY if isinstance(event, LongPositionOpened) else OrderSide.SELL

        entry_price = self._apply_slippage(position.entry_price, order_side)

        order = Order(side=order_side, price=entry_price, size=position.size)

        next_position = position.add_order(order).update_prices(order.price)
    
        await self.dispatcher.dispatch(OrderFilled(next_position))

    def _apply_slippage(self, price: float, order_side: OrderSide) -> float:
        factor = 1 + self.slippage

        if order_side == OrderSide.BUY:
            return price * factor
        elif order_side == OrderSide.SELL:
            return price / factor
