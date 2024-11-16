import asyncio
import logging
import random
from typing import TYPE_CHECKING, List, Optional, Tuple, Union

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
from core.models.entity.position import Position
from core.models.entity.profit_target import ProfitTarget
from core.models.entity.risk import Risk
from core.models.entity.signal import Signal
from core.models.side import PositionSide
from core.models.symbol import Symbol
from core.models.timeframe import Timeframe
from core.queries.ohlcv import TA, NextBar, PrevBar
from core.queries.portfolio import GetPortfolioPerformance

if TYPE_CHECKING:
    from core.models.entity.portfolio import Performance

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

SL_MULTI = 1.8


def _ema(values, alpha=0.1):
    ema = [values[0]]
    for value in values[1:]:
        ema.append(ema[-1] * (1 - alpha) + value * alpha)
    return np.array(ema)


logger = logging.getLogger(__name__)


class RiskActor(StrategyActor, EventHandlerMixin):
    def __init__(
        self, symbol: Symbol, timeframe: Timeframe, config_service: AbstractConfig
    ):
        super().__init__(symbol, timeframe)
        EventHandlerMixin.__init__(self)
        self._register_event_handlers()
        self._lock = asyncio.Lock()
        self._state: Tuple[Tuple[Risk, Position, ProfitTarget, Performance]] = (
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

            tp = pt.targets[3]
            sl = bar.close - SL_MULTI * pt.context_factor * volatility

            risk = Risk(ohlcv=[bar], side=side, tp=tp, sl=sl)
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
            states = list(self._state)
            num_states = len(self._state)

            indexes = list(range(num_states))
            random.shuffle(indexes)

            for shuffled_index in indexes:
                curr_state = self._state[shuffled_index]

                states[shuffled_index] = await self._process_market(event, curr_state)

            self._risk = tuple(states)

    async def _process_market(
        self,
        event: NewMarketDataReceived,
        state: Optional[Tuple[Risk, Position, ProfitTarget]],
    ):
        next_state = state

        if state:
            risk, position, pt, performance = state

            bars = await self._fetch_bars(event.bar.ohlcv, risk.curr_bar)

            for bar in sorted(bars, key=lambda x: x.timestamp):
                ts = np.array(risk.time_points)

                if len(ts) > 2:
                    ts_diff = _ema(np.diff(ts))
                    mean, std = np.mean(ts_diff), max(
                        np.std(ts_diff), np.finfo(float).eps
                    )

                    current_diff = abs(bar.timestamp - ts[-1])
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
                        continue
                    else:
                        self.anomaly_threshold = DEFAULT_ANOMALY_THRESHOLD
                        self.max_bars = DEFAULT_MAX_BARS
                        self.consc_anomaly_counter = 1

                risk = risk.next(bar, position.signal)

                next_state = (risk, position, pt, performance)

                if risk.has_risk:
                    open_signal = position.signal
                    exit_price = (
                        risk.curr_bar.high + risk.curr_bar.low + risk.curr_bar.close
                    ) / 3.0

                    signal = Signal(
                        symbol=open_signal.symbol,
                        timeframe=open_signal.timeframe,
                        strategy=open_signal.strategy,
                        side=open_signal.side,
                        ohlcv=risk.curr_bar,
                        exit=exit_price,
                    )

                    risk_cls = (
                        RiskLongThresholdBreached
                        if risk.side == PositionSide.LONG
                        else RiskShortThresholdBreached
                    )

                    await self.tell(risk_cls(signal))
                    break

        return next_state

    async def _fetch_bars(self, curr_bar: OHLCV, prev_bar: OHLCV) -> List[OHLCV]:
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

                if not next_bar:
                    break

                bars.append(next_bar)
                prev_bar = next_bar

        return list(set(bars))
