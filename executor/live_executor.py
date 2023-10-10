from typing import Union

from core.actors.base import BaseActor
from core.commands.broker import ClosePosition, OpenPosition
from core.events.position import (
    BrokerPositionClosed,
    BrokerPositionOpened,
    PositionCloseRequested,
    PositionInitialized,
)
from core.models.order import Order, OrderStatus
from core.models.position import Position
from core.models.strategy import Strategy
from core.models.symbol import Symbol
from core.models.timeframe import Timeframe
from core.queries.broker import GetOpenPosition

PositionEvent = Union[PositionInitialized, PositionCloseRequested]


class LiveExecutor(BaseActor):
    def __init__(self, symbol: Symbol, timeframe: Timeframe, strategy: Strategy):
        super().__init__(symbol, timeframe, strategy)

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

    async def _filter_event(self, event: PositionEvent):
        signal = event.position.signal
        return signal.symbol == self._symbol and signal.timeframe == self._timeframe

    async def _execute_order(self, position: Position):
        await self.execute(OpenPosition(position))

        broker_position = await self.query(GetOpenPosition(position.signal.symbol))
        order = Order(
            status=OrderStatus.EXECUTED,
            size=broker_position["position_size"],
            price=broker_position["entry_price"],
        )

        next_position = position.add_order(order).update_prices(order.price)

        await self.dispatch(BrokerPositionOpened(next_position))

    async def _close_position(self, position: Position):
        await self.execute(ClosePosition(position))
        await self.dispatch(BrokerPositionClosed(position))
