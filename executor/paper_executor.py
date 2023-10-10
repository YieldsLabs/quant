from typing import Union

from core.actors.base import BaseActor
from core.events.position import (
    BrokerPositionClosed,
    BrokerPositionOpened,
    PositionCloseRequested,
    PositionInitialized,
)
from core.models.order import Order, OrderStatus
from core.models.position import Position, PositionSide
from core.models.strategy import Strategy
from core.models.symbol import Symbol
from core.models.timeframe import Timeframe

PositionEvent = Union[PositionInitialized, PositionCloseRequested]


class PaperExecutor(BaseActor):
    def __init__(
        self, symbol: Symbol, timeframe: Timeframe, strategy: Strategy, slippage: float
    ):
        super().__init__(symbol, timeframe, strategy)
        self.slippage = slippage

    async def start(self):
        await super().start()

        for event in [PositionInitialized, PositionCloseRequested]:
            self._dispatcher.register(event, self.handle, self._filter_event)

    async def stop(self):
        await super().stop()

        for event in [PositionInitialized, PositionCloseRequested]:
            self._dispatcher.unregister(event, self.handle)

    async def handle(self, event: PositionEvent):
        if isinstance(event, PositionInitialized):
            return await self._execute_order(event.position)
        elif isinstance(event, PositionCloseRequested):
            return await self._close_position(event.position)

    def _filter_event(self, event: PositionEvent):
        signal = event.position.signal
        return signal.symbol == self._symbol and signal.timeframe == self._timeframe

    async def _execute_order(self, position: Position):
        entry_price = self._apply_slippage(position, 1 + self.slippage)

        order = Order(
            status=OrderStatus.EXECUTED, price=entry_price, size=position.size
        )

        next_position = position.add_order(order).update_prices(order.price)

        await self.dispatch(BrokerPositionOpened(next_position))

    async def _close_position(self, position: Position):
        await self.dispatch(BrokerPositionClosed(position))

    @staticmethod
    def _apply_slippage(position: Position, factor: float) -> float:
        if position.side == PositionSide.LONG:
            return position.entry_price * factor
        elif position.side == PositionSide.SHORT:
            return position.entry_price / factor
