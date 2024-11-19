import asyncio
import logging
from typing import List, Tuple, Union

import numpy as np

from core.actors import StrategyActor
from core.actors.state import InMemory
from core.events.market import NewMarketDataReceived
from core.events.position import (
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
    PositionClosed,
]

MAX_ATTEMPTS = 8
DEFAULT_MAX_BARS = 12
MAX_CONSECUTIVE_ANOMALIES = 3
DYNAMIC_THRESHOLD_MULTIPLIER = 8.0
DEFAULT_ANOMALY_THRESHOLD = 6.0
ANOMALY_CLIP_MULTIPLIER = 12.0
LATENCY_GAP_THRESHOLD = 2.2
SL_MULTI = 1.5
RRR_MULTI = 2.0
BAR_TIMEOUT = 15


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

        self._state = InMemory[PositionSide, RiskState]()
        self._locks = {
            PositionSide.LONG: asyncio.Semaphore(1),
            PositionSide.SHORT: asyncio.Semaphore(1),
        }

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
        position = event.position
        side = position.side
        bar = position.open_bar
        open_signal = position.signal

        ta = await self.ask(TA(self.symbol, self.timeframe, bar))

        rolling_window = 8
        volatility = np.convolve(
            ta.volatility.tr, np.ones(rolling_window) / rolling_window, mode="valid"
        )[-1]

        pt = ProfitTarget(side=side, entry=position.entry_price, volatility=volatility)

        performance = await self.ask(
            GetPortfolioPerformance(
                self.symbol, self.timeframe, position.signal.strategy
            )
        )

        price = bar.low if position.side == PositionSide.LONG else bar.high
        volatility_factor = volatility * SL_MULTI
        sl = (
            price - volatility_factor
            if position.side == PositionSide.LONG
            else price + volatility_factor
        )

        risk_factor = RRR_MULTI * abs(position.entry_price - sl)
        tp = (
            price + risk_factor
            if position.side == PositionSide.LONG
            else price - risk_factor
        )

        trade_duration = self.config.get("trade_duration", 20)

        risk = Risk(side=side, tp=tp, sl=sl, duration=trade_duration).next(bar)

        logger.info(
            f"SIDE: {side}, BAR: {bar}, TP: {tp}, SL: {sl}, RISK: {risk.has_risk}"
        )

        state = None

        if not risk.has_risk:
            state = (risk, position, pt, performance)
        else:
            close_signal = Signal(
                symbol=open_signal.symbol,
                timeframe=open_signal.timeframe,
                strategy=open_signal.strategy,
                side=open_signal.side,
                ohlcv=bar,
                entry=open_signal.entry,
                exit=bar.close,
            )

            event = (
                RiskLongThresholdBreached(signal=close_signal)
                if side == PositionSide.LONG
                else RiskShortThresholdBreached(signal=close_signal)
            )

            await self.tell(event)

        await self._state.set(side, state)

    async def _close_position(self, event: PositionClosed):
        await self._state.delete(event.position.side)

    async def _handle_risk(self, event: NewMarketDataReceived):
        sides = list(PositionSide)
        tasks = [self._process_side(side, event) for side in sides]
        await asyncio.gather(*tasks)

    async def _process_side(self, side, event):
        async with self._locks.get(side):
            await self._process_market(event, side)

    async def _process_market(
        self,
        event: NewMarketDataReceived,
        side: PositionSide,
    ):
        state = await self._state.get(side)

        if not state:
            return

        risk, position, pt, performance = state

        if risk.has_risk:
            return

        next_risk = risk
        open_signal = position.signal
        cbar = next_risk.curr_bar

        processed_timestamps = set()

        bars = await self._fetch_bars(event.bar.ohlcv, cbar)

        if not bars:
            logger.warning("No bars fetched, skipping market processing.")
            return state

        for bar in bars:
            if bar.timestamp in processed_timestamps:
                logger.info(f"Duplicate bar skipped: {bar.timestamp}")
                continue

            processed_timestamps.add(bar.timestamp)

            if self._has_anomaly(bar.timestamp, next_risk.time_points):
                logger.info(f"Anomalous bar skipped: {bar.timestamp}")
                continue

            gap = bar.timestamp - cbar.timestamp

            if gap <= 0:
                logger.info(f"Stale bar skipped: {bar.timestamp}")
                continue

            if gap > LATENCY_GAP_THRESHOLD * open_signal.timeframe.to_milliseconds():
                logger.info(f"Latency Gap: {gap} exceeds threshold.")
                continue

            next_risk = next_risk.next(bar)

            cbar = next_risk.curr_bar

            if next_risk.has_risk:
                logger.info("Risk threshold breached, triggering position close.")
                break

        next_price = (cbar.high + cbar.low + cbar.close) / 3.0

        if next_risk.has_risk:
            close_signal = Signal(
                symbol=open_signal.symbol,
                timeframe=open_signal.timeframe,
                strategy=open_signal.strategy,
                side=open_signal.side,
                ohlcv=cbar,
                entry=open_signal.entry,
                exit=next_price,
            )

            event = (
                RiskLongThresholdBreached(signal=close_signal)
                if side == PositionSide.LONG
                else RiskShortThresholdBreached(signal=close_signal)
            )

            await self.tell(event)

        pnl = pt.context_factor * (next_price - position.entry_price) * position.size
        ap = performance.next(pnl, position.fee)

        logger.info(
            f"{cbar.timestamp}:{open_signal.symbol}:{side} -> "
            f"PnL: {pnl:.4f}, VAR: {ap.mvar:.4f}, MDD: {ap.max_drawdown * 100:.4f}, H: {cbar.high}, L: {cbar.low}, CPR: {next_price:.4f}, TP: {next_risk.tp:.4f}, SL: {next_risk.sl:.4f}"
        )

        next_state = (next_risk, position, pt, performance)

        await self._state.set(side, next_state)

    def _has_anomaly(self, bar_timestamp: float, time_points: list[float]) -> bool:
        if len(time_points) <= 2:
            return False

        time_points = np.array(time_points)

        ts_diff = _ema(np.diff(time_points))
        mean, std = np.mean(ts_diff), max(np.std(ts_diff), np.finfo(float).eps)

        current_diff = abs(bar_timestamp - time_points[-1])
        anomaly_score = (current_diff - mean) / std

        anomaly_score = np.clip(
            anomaly_score,
            -ANOMALY_CLIP_MULTIPLIER * DEFAULT_ANOMALY_THRESHOLD,
            ANOMALY_CLIP_MULTIPLIER * DEFAULT_ANOMALY_THRESHOLD,
        )

        if abs(anomaly_score) > self.anomaly_threshold:
            self.consc_anomaly_counter += 1

            if self.consc_anomaly_counter > MAX_CONSECUTIVE_ANOMALIES:
                logger.warning(
                    "Too many consecutive anomalies detected. "
                    f"Increasing thresholds: anomaly_threshold={self.anomaly_threshold}, "
                    f"max_bars={self.max_bars}"
                )
                self.anomaly_threshold *= DYNAMIC_THRESHOLD_MULTIPLIER
                self.max_bars *= DYNAMIC_THRESHOLD_MULTIPLIER
                self.consc_anomaly_counter = 0

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

        attempts = 0

        while (
            next_bar
            and next_bar.timestamp == curr_bar.timestamp
            and attempts < MAX_ATTEMPTS
        ):
            next_bar = await self.ask(NextBar(self.symbol, self.timeframe, curr_bar))
            attempts += 1

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

                if next_bar and next_bar.timestamp > bars[-1].timestamp:
                    if next_bar.timestamp not in [bar.timestamp for bar in bars]:
                        bars.append(next_bar)

                    prev_bar = next_bar

        return bars
