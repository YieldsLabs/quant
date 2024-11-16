import asyncio
import logging
import random
from typing import List, Optional, Tuple, Union

import numpy as np

from core.actors import StrategyActor
from core.events.market import NewMarketDataReceived
from core.events.position import (
    PositionAdjusted,
    PositionClosed,
    PositionOpened,
)
from core.events.risk import (
    RiskLongThresholdBreached,
    RiskShortThresholdBreached,
)
from core.events.signal import (
    ExitLongSignalReceived,
    ExitShortSignalReceived,
    GoLongSignalReceived,
    GoShortSignalReceived,
)
from core.interfaces.abstract_config import AbstractConfig
from core.mixins import EventHandlerMixin
from core.models.entity.ohlcv import OHLCV
from core.models.entity.portfolio import Performance
from core.models.entity.position import Position
from core.models.entity.profit_target import ProfitTarget
from core.models.entity.risk import Risk
from core.models.entity.signal import Signal
from core.models.side import PositionSide
from core.models.symbol import Symbol
from core.models.timeframe import Timeframe
from core.queries.ohlcv import TA, NextBar, PrevBar
from core.queries.portfolio import GetPortfolioPerformance

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
LATENCY_GAP_THRESHOLD = 2.2
SL_MULTI = 1.8


def _ema(values, alpha=0.1):
    ema = [values[0]]
    for value in values[1:]:
        ema.append(ema[-1] * (1 - alpha) + value * alpha)
    return np.array(ema)


logger = logging.getLogger(__name__)

RiskState = Tuple[Risk, Position, ProfitTarget, Performance]


class RiskActor(StrategyActor, EventHandlerMixin):
    def __init__(
        self, symbol: Symbol, timeframe: Timeframe, config_service: AbstractConfig
    ):
        super().__init__(symbol, timeframe)
        EventHandlerMixin.__init__(self)
        self._register_event_handlers()
        self._lock = asyncio.Lock()
        self._state: Tuple[RiskState] = (
            None,
            None,
        )
        self.config = config_service.get("position")
        self.max_bars = DEFAULT_MAX_BARS
        self.anomaly_threshold = DEFAULT_ANOMALY_THRESHOLD
        self.consc_anomaly_counter = 1

    async def on_receive(self, event: RiskEvent):
        return await self.handle_event(event)

    def _register_event_handlers(self):
        self.register_handler(NewMarketDataReceived, self._handle_risk)
        self.register_handler(PositionOpened, self._open_position)
        self.register_handler(PositionClosed, self._close_position)

    async def _open_position(self, event: PositionOpened):
        async with self._lock:
            position = event.position
            side = position.side
            bar = position.open_bar

            ta = await self.ask(TA(self.symbol, self.timeframe, bar))
            volatility = ta.volatility.yz[-1]

            pt = ProfitTarget(
                side=side, entry=position.entry_price, volatility=volatility
            )

            tp = pt.targets[-1]
            sl = bar.close - SL_MULTI * pt.context_factor * volatility

            print(f"SIDE: {side}, BAR: {bar}, TP: {tp}, SL: {sl}")

            risk = Risk(side=side, tp=tp, sl=sl)
            risk = risk.next(bar)

            performance = await self.ask(
                GetPortfolioPerformance(
                    self.symbol, self.timeframe, position.signal.strategy
                )
            )

            state = (risk, position, pt, performance)

            match side:
                case PositionSide.LONG:
                    self._state = (state, self._state[1])
                case PositionSide.SHORT:
                    self._state = (self._state[0], state)

    async def _close_position(self, event: PositionClosed):
        async with self._lock:
            match event.position.side:
                case PositionSide.LONG:
                    self._state = (None, self._state[1])
                case PositionSide.SHORT:
                    self._state = (self._state[0], None)

    async def _handle_risk(self, event: NewMarketDataReceived):
        async with self._lock:
            current_states = list(self._state)
            num_states = len(current_states)

            updated_states = current_states[:]

            indexes = list(range(num_states))
            random.shuffle(indexes)

            for shuffled_index in indexes:
                curr_state = current_states[shuffled_index]

                updated_states[shuffled_index] = await self._process_market(
                    event, curr_state
                )

            self._state = tuple(updated_states)

    async def _process_market(
        self,
        event: NewMarketDataReceived,
        state: Optional[RiskState],
    ):
        if not state:
            return state

        risk, position, pt, performance = state

        if risk.has_risk:
            return state

        next_risk = risk
        open_signal = position.signal

        bars = await self._fetch_bars(event.bar.ohlcv, next_risk.curr_bar)

        if not bars:
            logger.warning("No bars fetched, skipping market processing.")
            return state

        for bar in bars:
            if self._has_anomaly(bar.timestamp, next_risk.time_points):
                logger.debug(f"Anomalous bar skipped: {bar.timestamp}")
                continue

            gap = bar.timestamp - next_risk.curr_bar.timestamp

            if gap <= 0:
                logger.debug(f"Stale bar skipped: {bar.timestamp}")
                continue

            if gap > LATENCY_GAP_THRESHOLD * open_signal.timeframe.to_milliseconds():
                logger.info(f"Latency Gap: {gap} exceeds threshold.")
                continue

            next_risk = next_risk.next(bar)

            if next_risk.has_risk:
                logger.info("Risk threshold breached, triggering position close.")
                break

        curr_bar = next_risk.curr_bar
        next_price = (curr_bar.high + curr_bar.low + curr_bar.close) / 3.0

        logger.info(
            f"{open_signal.symbol}:{position.side} -> "
            f"Bar: {curr_bar}, CPR: {next_price:.4f}, TP: {next_risk.tp:.4f}, SL: {next_risk.sl:.4f}"
        )

        if next_risk.has_risk:
            close_signal = Signal(
                symbol=open_signal.symbol,
                timeframe=open_signal.timeframe,
                strategy=open_signal.strategy,
                side=open_signal.side,
                ohlcv=curr_bar,
                exit=next_price,
            )

            risk_cls = (
                RiskLongThresholdBreached
                if risk.side == PositionSide.LONG
                else RiskShortThresholdBreached
            )

            await self.tell(risk_cls(close_signal))

        return (next_risk, position, pt, performance)

    def _has_anomaly(self, bar_timestamp: float, time_points: list[float]) -> bool:
        if len(time_points) <= 2:
            return False

        time_points = np.array(time_points)

        ts_diff = _ema(np.diff(time_points))
        mean, std = np.mean(ts_diff), max(np.std(ts_diff), np.finfo(float).eps)

        current_diff = abs(bar_timestamp - time_points[-1])
        anomaly = (current_diff - mean) / std
        anomaly = np.clip(
            anomaly,
            -12.0 * DEFAULT_ANOMALY_THRESHOLD,
            12.0 * DEFAULT_ANOMALY_THRESHOLD,
        )

        if abs(anomaly) > self.anomaly_threshold:
            self.consc_anomaly_counter += 1

            if self.consc_anomaly_counter > MAX_CONSECUTIVE_ANOMALIES:
                logger.warn(
                    "Too many consecutive anomalies, increasing threshold temporarily"
                )
                self.anomaly_threshold *= DYNAMIC_THRESHOLD_MULTIPLIER
                self.max_bars *= DYNAMIC_THRESHOLD_MULTIPLIER
                self.consc_anomaly_counter = 1

            return True

        self.anomaly_threshold = DEFAULT_ANOMALY_THRESHOLD
        self.max_bars = DEFAULT_MAX_BARS
        self.consc_anomaly_counter = 1

        return False

    async def _fetch_bars(self, event_bar: OHLCV, risk_bar: OHLCV) -> List[OHLCV]:
        bars = []
        prev_bar = min(event_bar, risk_bar)
        curr_bar = max(event_bar, risk_bar)

        next_bar = await self.ask(NextBar(self.symbol, self.timeframe, prev_bar))

        next_bar = next_bar or curr_bar

        attempts = 0
        diff = curr_bar.timestamp - next_bar.timestamp

        while diff < 0 and attempts < MAX_ATTEMPTS:
            new_prev_bar = await self.ask(
                PrevBar(self.symbol, self.timeframe, prev_bar)
            )

            if new_prev_bar:
                diff = curr_bar.timestamp - new_prev_bar.timestamp
                prev_bar = new_prev_bar

            attempts += 1

        bars = [next_bar]

        if diff > 0:
            for _ in range(int(self.max_bars)):
                next_bar = await self.ask(
                    NextBar(self.symbol, self.timeframe, prev_bar)
                )

                if not next_bar or next_bar.timestamp <= bars[-1].timestamp:
                    continue

                bars.append(next_bar)
                bars = sorted(bars, key=lambda x: x.timestamp)

                prev_bar = next_bar

        return bars
