import asyncio
from typing import Optional, Union

from core.actors import Actor
from core.events.ohlcv import NewMarketDataReceived
from core.events.position import (
    PositionAdjusted,
    PositionClosed,
    PositionOpened,
)
from core.events.risk import RiskThresholdBreached
from core.events.signal import (
    ExitLongSignalReceived,
    ExitShortSignalReceived,
    GoLongSignalReceived,
    GoShortSignalReceived,
)
from core.interfaces.abstract_config import AbstractConfig
from core.interfaces.abstract_market_repository import AbstractMarketRepository
from core.models.position import Position
from core.models.side import PositionSide
from core.models.symbol import Symbol
from core.models.timeframe import Timeframe

RiskEvent = Union[
    NewMarketDataReceived,
    PositionOpened,
    PositionAdjusted,
    PositionClosed,
    ExitLongSignalReceived,
    ExitShortSignalReceived,
    GoLongSignalReceived,
    GoShortSignalReceived,
]

TrailEvent = Union[
    ExitLongSignalReceived,
    ExitShortSignalReceived,
    GoLongSignalReceived,
    GoShortSignalReceived,
]


class RiskActor(Actor):
    _EVENTS = [
        NewMarketDataReceived,
        PositionOpened,
        PositionClosed,
        ExitLongSignalReceived,
        ExitShortSignalReceived,
        GoLongSignalReceived,
        GoShortSignalReceived,
    ]

    def __init__(
        self,
        symbol: Symbol,
        timeframe: Timeframe,
        config_service: AbstractConfig,
        repository: AbstractMarketRepository,
    ):
        super().__init__(symbol, timeframe)
        self._lock = asyncio.Lock()
        self._position = (None, None)
        self.config = config_service.get("position")
        self._store = repository

    def pre_receive(self, event: RiskEvent):
        symbol, timeframe = self._get_event_key(event)
        return self.symbol == symbol and self.timeframe == timeframe

    async def on_receive(self, event: RiskEvent):
        handlers = {
            NewMarketDataReceived: [self._handle_market, self._handle_position_risk],
            PositionOpened: [self._open_position],
            PositionClosed: [self._close_position],
            ExitLongSignalReceived: [self._trail_position],
            ExitShortSignalReceived: [self._trail_position],
            GoLongSignalReceived: [self._trail_position],
            GoShortSignalReceived: [self._trail_position],
        }

        handler = handlers.get(type(event))

        if handler:
            for h in handler:
                await h(event)

    async def _open_position(self, event: PositionOpened):
        async with self._lock:
            long_position, short_position = self._position

            self._position = (
                event.position
                if event.position.side == PositionSide.LONG
                else long_position,
                event.position
                if event.position.side == PositionSide.SHORT
                else short_position,
            )

    async def _close_position(self, event: PositionClosed):
        async with self._lock:
            long_position, short_position = self._position

            self._position = (
                None if event.position.side == PositionSide.LONG else long_position,
                None if event.position.side == PositionSide.SHORT else short_position,
            )

    async def _handle_market(self, event: NewMarketDataReceived):
        await self._store.upsert(self.symbol, self.timeframe, event.ohlcv)

    async def _handle_position_risk(self, _event: NewMarketDataReceived):
        async with self._lock:
            long_position, short_position = self._position

            if long_position or short_position:
                long_position, short_position = await asyncio.gather(
                    *[
                        self._process_market(long_position),
                        self._process_market(short_position),
                    ]
                )

                self._position = (long_position, short_position)

    async def _trail_position(self, event: TrailEvent):
        async with self._lock:
            long_position, short_position = self._position

            if (
                isinstance(event, ExitLongSignalReceived)
                and long_position
                and not long_position.has_risk
            ):
                long_position = long_position.trail(event.signal.exit)

            if (
                isinstance(event, ExitShortSignalReceived)
                and short_position
                and not short_position.has_risk
            ):
                short_position = short_position.trail(event.signal.exit)

            if (
                isinstance(event, GoLongSignalReceived)
                and short_position
                and not short_position.has_risk
            ):
                short_position = short_position.trail()

            if (
                isinstance(event, GoShortSignalReceived)
                and long_position
                and not long_position.has_risk
            ):
                long_position = long_position.trail()

            self._position = (long_position, short_position)

    async def _process_market(self, position: Optional[Position]):
        next_position = position

        if position and not position.has_risk:
            async for next_bar in self._store.find_next_bar(
                self.symbol, self.timeframe, next_position.risk_bar
            ):
                if not next_bar:
                    continue

                next_position = next_position.next(next_bar)

                if next_position.has_risk:
                    await self.tell(RiskThresholdBreached(next_position))
                    break

        return next_position

    @staticmethod
    def _get_event_key(event: RiskEvent):
        signal = (
            event.signal
            if hasattr(event, "signal")
            else event.position.signal
            if hasattr(event, "position")
            else event
        )

        return (signal.symbol, signal.timeframe)
