import asyncio
import random
from typing import Optional, Union

import numpy as np

from core.actors import StrategyActor
from core.events.base import EventMeta
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

MAX_ATTEMPTS = 16
DEFAULT_MAX_BARS = 16
MAX_CONSECUTIVE_ANOMALIES = 3
DYNAMIC_THRESHOLD_MULTIPLIER = 8.0
DEFAULT_ANOMALY_THRESHOLD = 6.0


def _ema(values, alpha=0.1):
    ema = [values[0]]
    for value in values[1:]:
        ema.append(ema[-1] * (1 - alpha) + value * alpha)
    return np.array(ema)


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
        self.max_bars = DEFAULT_MAX_BARS
        self.anomaly_threshold = DEFAULT_ANOMALY_THRESHOLD
        self.consc_anomaly_counter = 1

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
            if event.position.side == PositionSide.LONG:
                self._position = (event.position, self._position[1])
            elif event.position.side == PositionSide.SHORT:
                self._position = (self._position[0], event.position)

    async def _close_position(self, event: PositionClosed):
        async with self._lock:
            if event.position.side == PositionSide.LONG:
                self._position = (None, self._position[1])
            elif event.position.side == PositionSide.SHORT:
                self._position = (self._position[0], None)

    async def _handle_position_risk(self, event: NewMarketDataReceived):
        async with self._lock:
            processed_positions = list(self._position)
            num_positions = len(self._position)
            
            current_index = 0
            
            for _ in range(num_positions):
                processed_positions[current_index] = await self._process_market(event, self._position[current_index])
                
                current_index = (current_index + 1) % num_positions

            self._position = tuple(processed_positions)
    
    async def _trail_position(self, event: TrailEvent):
        async with self._lock:
            long_position, short_position = self._position

            async def handle_trail(position: Position, risk_bar: OHLCV):
                ta = await self.ask(TA(self.symbol, self.timeframe, risk_bar))
                return position.trail(ta)

            async def process_trail(position: Position, event_meta: EventMeta):
                if position and not position.has_risk and position.last_modified < event_meta.timestamp:
                    return await handle_trail(position, position.risk_bar)
                return position

            if isinstance(event, (ExitLongSignalReceived, GoShortSignalReceived)):
                long_position = await process_trail(long_position, event.meta)

            elif isinstance(event, (ExitShortSignalReceived, GoLongSignalReceived)):
                short_position = await process_trail(short_position, event.meta)

            self._position = (long_position, short_position)

    async def _process_market(
        self, event: NewMarketDataReceived, position: Optional[Position]
    ):
        next_position = position

        if position and not position.has_risk:
            prev_bar = next_position.risk_bar
            next_bar = await self.ask(NextBar(self.symbol, self.timeframe, prev_bar))

            if not next_bar:
                next_bar = event.ohlcv

            diff = event.ohlcv.timestamp - next_bar.timestamp
            attempts = 0

            while diff < 0 and attempts < MAX_ATTEMPTS:
                new_prev_bar = await self.ask(
                    PrevBar(self.symbol, self.timeframe, prev_bar)
                )
                attempts += 1

                if new_prev_bar:
                    diff = event.ohlcv.timestamp - new_prev_bar.timestamp
                    prev_bar = new_prev_bar

            bars = [next_bar]

            if diff > 0:
                for _ in range(int(self.max_bars)):
                    next_bar = await self.ask(
                        NextBar(self.symbol, self.timeframe, prev_bar)
                    )

                    if not next_bar:
                        break

                    bars.append(next_bar)
                    prev_bar = next_bar

            for bar in sorted(bars, key=lambda x: x.timestamp):
                ohlcv = next_position.position_risk.ohlcv
                ts = np.array([o.timestamp for o in ohlcv])

                if len(ts) > 2:
                    ts_diff = _ema(np.diff(ts))
                    mean, std = np.mean(ts_diff), max(
                        np.std(ts_diff), np.finfo(float).eps
                    )

                    current_diff = abs(bar.timestamp - ts[-1])
                    anomaly = (current_diff - mean) / std
                    anomaly = np.clip(
                        anomaly,
                        -9.0 * DEFAULT_ANOMALY_THRESHOLD,
                        9.0 * DEFAULT_ANOMALY_THRESHOLD,
                    )

                    if abs(anomaly) > self.anomaly_threshold:
                        self.consc_anomaly_counter += 1

                        if self.consc_anomaly_counter > MAX_CONSECUTIVE_ANOMALIES:
                            print(
                                "Too many consecutive anomalies, increasing threshold temporarily"
                            )
                            self.anomaly_threshold *= DYNAMIC_THRESHOLD_MULTIPLIER
                            self.max_bars *= DYNAMIC_THRESHOLD_MULTIPLIER
                            self.consc_anomaly_counter = 1
                        await asyncio.sleep(0.00001)
                        continue
                    else:
                        self.anomaly_threshold = DEFAULT_ANOMALY_THRESHOLD
                        self.max_bars = DEFAULT_MAX_BARS
                        self.consc_anomaly_counter = 1

                ta = await self.ask(TA(self.symbol, self.timeframe, bar))
                session_risk = await self.ask(
                    EvaluateSession(next_position.side, ohlcv, ta)
                )

                next_position = next_position.next(bar, ta, session_risk)

                if next_position.has_risk:
                    await self.tell(RiskThresholdBreached(next_position))
                    break

        return next_position
