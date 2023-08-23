from typing import Union

from core.event_decorators import event_handler
from core.events.position import LongPositionOpened, ShortPositionOpened, OrderFilled
from core.models.order import Order, OrderSide
from core.interfaces.abstract_executor import AbstractExecutor


class PaperExecutor(AbstractExecutor):
    def __init__(self, slippage: float):
        super().__init__()
        self.slippage = slippage

    @event_handler(LongPositionOpened)
    async def _on_long_position(self, event: LongPositionOpened):
        await self.execute_order(event)

    @event_handler(ShortPositionOpened)
    async def _on_short_position(self, event: ShortPositionOpened):
        await self.execute_order(event)

    async def execute_order(self, event: Union[LongPositionOpened, ShortPositionOpened]):
        order_side = OrderSide.BUY if isinstance(event, LongPositionOpened) else OrderSide.SELL

        entry_price = self._apply_slippage(event.entry, order_side)

        order = Order(side=order_side, price=entry_price, size=event.size)

        await self.dispatcher.dispatch(
            OrderFilled(strategy=event.strategy, order=order))

    def _apply_slippage(self, price: float, order_side: OrderSide) -> float:
        factor = 1 + self.slippage

        if order_side == OrderSide.BUY:
            return price * factor
        elif order_side == OrderSide.SELL:
            return price / factor
