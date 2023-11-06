from typing import Union

from core.actors.base import BaseActor
from core.commands.broker import ClosePosition, OpenPosition
from core.events.position import (
    BrokerPositionClosed,
    BrokerPositionOpened,
    PositionCloseRequested,
    PositionInitialized,
)
from core.models.position import Position
from core.models.strategy import Strategy
from core.models.symbol import Symbol
from core.models.timeframe import Timeframe
from core.queries.broker import GetOpenPosition

PositionEventType = Union[PositionInitialized, PositionCloseRequested]


class MarketOrderExecutor(BaseActor):
    _EVENTS = [PositionInitialized, PositionCloseRequested]

    def __init__(self, symbol: Symbol, timeframe: Timeframe, strategy: Strategy):
        super().__init__(symbol, timeframe, strategy)

    async def start(self):
        await super().start()

        for event in self._EVENTS:
            self._dispatcher.register(event, self.handle, self._filter_event)

    async def stop(self):
        await super().stop()

        for event in self._EVENTS:
            self._dispatcher.unregister(event, self.handle)

    async def handle(self, event: PositionEventType):
        handlers = {
            PositionInitialized: self._execute_order,
            PositionCloseRequested: self._close_position,
        }

        handler = handlers.get(type(event))

        if handler:
            await handler(event.position)

    def _filter_event(self, event: PositionEventType):
        signal = event.position.signal
        return signal.symbol == self._symbol and signal.timeframe == self._timeframe

    async def _execute_order(self, position: Position):
        await self.execute(OpenPosition(position))

        next_position = await self.query(GetOpenPosition(position))

        await self.dispatch(BrokerPositionOpened(next_position))

    async def _close_position(self, position: Position):
        await self.execute(ClosePosition(position))
        await self.dispatch(BrokerPositionClosed(position))
