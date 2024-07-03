import asyncio
from typing import Optional, Union

import numpy as np

from core.actors import StrategyActor
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
from core.mixins import EventHandlerMixin
from core.models.ohlcv import OHLCV
from core.models.position import Position
from core.models.side import PositionSide
from core.models.symbol import Symbol
from core.models.timeframe import Timeframe
from core.queries.copilot import EvaluateSession
from core.queries.ohlcv import TA, NextBar, PrevBar

TrailEvent = Union[
    GoLongSignalReceived,
    GoShortSignalReceived,
    ExitLongSignalReceived,
    ExitShortSignalReceived,
]

RiskEvent = Union[
    NewMarketDataReceived,
    PositionOpened,
    PositionAdjusted,
    PositionClosed,
    TrailEvent,
]


class RiskActor(StrategyActor, EventHandlerMixin):
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
        self, symbol: Symbol, timeframe: Timeframe, config_service: AbstractConfig
    ):
        super().__init__(symbol, timeframe)
        EventHandlerMixin.__init__(self)
        self._register_event_handlers()
        self._lock = asyncio.Lock()
        self._position = (None, None)
        self.config = config_service.get("position")

    async def on_receive(self, event: RiskEvent):
        return await self.handle_event(event)

    def _register_event_handlers(self):
        self.register_handler(NewMarketDataReceived, self._handle_position_risk)
        self.register_handler(PositionOpened, self._open_position)
        self.register_handler(PositionClosed, self._close_position)
        self.register_handler(ExitLongSignalReceived, self._trail_position)
        self.register_handler(ExitShortSignalReceived, self._trail_position)
        self.register_handler(GoLongSignalReceived, self._trail_position)
        self.register_handler(GoShortSignalReceived, self._trail_position)

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

    async def _handle_position_risk(self, event: NewMarketDataReceived):
        async with self._lock:
            long_position, short_position = self._position

            if long_position or short_position:
                long_position, short_position = await asyncio.gather(
                    *[
                        self._process_market(event, long_position),
                        self._process_market(event, short_position),
                    ]
                )

                self._position = (long_position, short_position)

    async def _trail_position(self, event: TrailEvent):
        async with self._lock:
            long_position, short_position = self._position

            async def handle_trail(position: Position, risk_bar: OHLCV):
                ta = await self.ask(TA(self.symbol, self.timeframe, risk_bar))
                return position.trail(ta)

            if isinstance(event, ExitLongSignalReceived):
                if (
                    long_position
                    and not long_position.has_risk
                    and long_position.last_modified < event.meta.timestamp
                ):
                    long_position = await handle_trail(
                        long_position, long_position.risk_bar
                    )

            elif isinstance(event, ExitShortSignalReceived):
                if (
                    short_position
                    and not short_position.has_risk
                    and short_position.last_modified < event.meta.timestamp
                ):
                    short_position = await handle_trail(
                        short_position, short_position.risk_bar
                    )

            elif isinstance(event, GoLongSignalReceived):
                if (
                    short_position
                    and not short_position.has_risk
                    and short_position.last_modified < event.meta.timestamp
                ):
                    short_position = await handle_trail(
                        short_position, short_position.risk_bar
                    )

            elif isinstance(event, GoShortSignalReceived):
                if (
                    long_position
                    and not long_position.has_risk
                    and long_position.last_modified < event.meta.timestamp
                ):
                    long_position = await handle_trail(
                        long_position, long_position.risk_bar
                    )

            self._position = (long_position, short_position)

    async def _process_market(
        self, event: NewMarketDataReceived, position: Optional[Position]
    ):
        next_position = position

        if position and not position.has_risk:
            prev_bar = next_position.risk_bar
            next_bar = await self.ask(NextBar(self.symbol, self.timeframe, prev_bar))

            if not next_bar:
                return next_position

            diff = event.ohlcv.timestamp - next_bar.timestamp

            if diff < 0:
                while diff < 0:
                    new_prev_bar = await self.ask(
                        PrevBar(self.symbol, self.timeframe, prev_bar)
                    )

                    if new_prev_bar:
                        diff = event.ohlcv.timestamp - new_prev_bar.timestamp
                        prev_bar = new_prev_bar

            bars = [next_bar]

            if diff > 0:
                for _ in range(4):
                    next_bar = await self.ask(
                        NextBar(self.symbol, self.timeframe, prev_bar)
                    )

                    if not next_bar:
                        break

                    bars.append(next_bar)
                    prev_bar = next_bar

            print(f"BARS: {len(bars)}")

            for bar in sorted(bars, key=lambda x: x.timestamp):
                ohlcv = next_position.position_risk.ohlcv
                ts = np.array([o.timestamp for o in ohlcv])

                if len(ts) > 2:
                    ts_diff = np.diff(ts)
                    mean_diff = np.mean(ts_diff)
                    std_diff = np.std(ts_diff)
                    current_diff = abs(bar.timestamp - ts[-1])

                    if std_diff == 0:
                        std_diff = 0.00000001

                    anomaly = (current_diff - mean_diff) / std_diff

                    print(f"Current score: {anomaly}")

                    if abs(anomaly) > 3:
                        print("Anomalyyyyy")
                        break

                ta = await self.ask(TA(self.symbol, self.timeframe, bar))

                session_risk = await self.ask(
                    EvaluateSession(next_position.side, ohlcv, ta)
                )

                next_position = next_position.next(bar, ta, session_risk)

                if next_position.has_risk:
                    await self.tell(RiskThresholdBreached(next_position))
                    break

        return next_position
