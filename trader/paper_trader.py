from typing import Union

from core.event_decorators import register_handler
from core.events.position import PositionClosed, LongPositionOpened, ShortPositionOpened, ClosePositionPrepared, OrderFilled
from core.position import Order, OrderSide

from .abstract_trader import AbstractTrader


TradeEvent = Union[LongPositionOpened, ShortPositionOpened]


class PaperTrader(AbstractTrader):
    def __init__(self, slippage: float = 0.01):
        super().__init__()
        self.slippage = slippage

    @register_handler(LongPositionOpened)
    async def _open_long_position(self, event: LongPositionOpened):
        await self.trade(event)

    @register_handler(ShortPositionOpened)
    async def _open_short_position(self, event: ShortPositionOpened):
        await self.trade(event)

    @register_handler(ClosePositionPrepared)
    async def _on_close_position(self, event: ClosePositionPrepared):
        await self.dispatcher.dispatch(
            PositionClosed(symbol=event.symbol, timeframe=event.timeframe, exit_price=event.exit_price))

    async def trade(self, event: TradeEvent):
        order_side = OrderSide.BUY if isinstance(event, LongPositionOpened) else OrderSide.SELL

        entry_price = self._apply_slippage(event.entry, order_side)

        order = Order(side=order_side, price=entry_price, size=event.size, stop_loss=event.stop_loss)

        await self.dispatcher.dispatch(
            OrderFilled(symbol=event.symbol, timeframe=event.timeframe, order=order))

    def _apply_slippage(self, price: float, order_side: OrderSide) -> float:
        factor = 1 + self.slippage

        if order_side == OrderSide.BUY:
            return price * factor
        elif order_side == OrderSide.SELL:
            return price / factor
