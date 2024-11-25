import asyncio
import logging
from typing import Tuple, Union

import numpy as np
from scipy.optimize import linprog

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
from core.interfaces.abstract_config import AbstractConfig
from core.mixins import EventHandlerMixin
from core.models.entity.portfolio import Performance
from core.models.entity.position import Position
from core.models.entity.profit_target import ProfitTarget
from core.models.entity.risk import Risk
from core.models.entity.signal import Signal
from core.models.side import PositionSide
from core.models.symbol import Symbol
from core.models.timeframe import Timeframe
from core.queries.ohlcv import TA, BatchBars
from core.queries.portfolio import GetPortfolioPerformance

RiskEvent = Union[
    NewMarketDataReceived,
    PositionOpened,
    PositionClosed,
]

MAX_ATTEMPTS = 8
DEFAULT_MAX_BARS = 18
MAX_CONSECUTIVE_ANOMALIES = 3
DYNAMIC_THRESHOLD_MULTIPLIER = 8.0
DEFAULT_ANOMALY_THRESHOLD = 6.0
ANOMALY_CLIP_MULTIPLIER = 12.0
ANOMALY_CLIP = ANOMALY_CLIP_MULTIPLIER * DEFAULT_ANOMALY_THRESHOLD
LATENCY_GAP_THRESHOLD = 2.2

VOLATILITY_MULTY = 1.5
RR_MULTY = 2.0


def _ema(values, alpha=0.1):
    values = np.asarray(values)
    weights = (1 - alpha) ** np.arange(len(values))[::-1]
    weights /= weights.sum()
    return np.convolve(values, weights, mode="full")[: len(values)]


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
        self.register_handler(PositionOpened, self._handle_opened_position)
        self.register_handler(PositionClosed, self._handle_closed_position)

    async def _handle_opened_position(self, event: PositionOpened):
        position = event.position
        side = position.side
        bar = position.open_bar
        open_signal = position.signal

        ta_result, perf_result = await asyncio.gather(
            self.ask(TA(self.symbol, self.timeframe, bar)),
            self.ask(
                GetPortfolioPerformance(
                    self.symbol, self.timeframe, position.signal.strategy
                )
            ),
        )

        if ta_result.is_err() or perf_result.is_err():
            await self._close_position(open_signal, side, bar)
            return

        ta = ta_result.unwrap()
        performance = perf_result.unwrap()

        rolling_window = 8

        volatility = np.convolve(
            ta.volatility.tr, np.ones(rolling_window) / rolling_window, mode="valid"
        )[-1]

        base_sl = VOLATILITY_MULTY * volatility
        base_tp = RR_MULTY * base_sl

        dmi = ta.trend.dmi[-1]
        cci = ta.momentum.cci[-1]
        vwap = ta.volume.vwap[-1]
        rsi = ta.oscillator.srsi[-1]
        w_rsi, w_cci, w_dmi, w_vwap = 0.3, 0.25, 0.25, 0.2

        rsi_norm = max(0, min((rsi - 30) / (70 - 30), 1))
        cci_norm = max(0, min((cci + 100) / (200), 1))
        dmi_norm = max(0, min(dmi / 50, 1))
        distance_vwap = abs(bar.close - vwap)
        max_distance = 10
        vwap_norm = max(0, min(distance_vwap / max_distance, 1))

        score = (
            w_rsi * rsi_norm
            + w_cci * cci_norm
            + w_dmi * dmi_norm
            + w_vwap * (1 - vwap_norm)
        )

        sl_ad_coeff = 0.4
        tp_ad_coeff = 0.3

        c = [1, -1]
        A = [[-1, 0], [0, 1]]
        b = [
            -(base_sl * (1 + (score - 0.5) * sl_ad_coeff)),
            base_tp * (1 - abs(score - 0.5) * tp_ad_coeff),
        ]

        bounds = [(0, None), (0, None)]

        result = linprog(c, A_ub=A, b_ub=b, bounds=bounds, method="highs")

        if result.success:
            sl_final = result.x[0]
            tp_final = result.x[1]
        else:
            logger.warn("LP optimization failed, used fallback")
            sl_final = base_sl
            tp_final = base_tp

        if side == PositionSide.LONG:
            sl = bar.low - sl_final
            tp = bar.high + tp_final
        elif side == PositionSide.SHORT:
            sl = bar.high + sl_final
            tp = bar.low - tp_final

        trade_duration = self.config.get("trade_duration", 20)

        risk = Risk(side=side, tp=tp, sl=sl, duration=trade_duration).next(bar)

        logger.info(
            f"SIDE: {side}, BAR: {bar}, TP: {tp}, SL: {sl}, RISK: {risk.has_risk}"
        )

        if risk.has_risk:
            await self._close_position(open_signal, side, bar)
            return

        pt = ProfitTarget(side=side, entry=position.entry_price, volatility=volatility)

        state = (risk, position, pt, performance)
        await self._state.set(side, state)

    async def _handle_closed_position(self, event: PositionClosed):
        await self._state.delete(event.position.side)

    async def _handle_risk(self, event: NewMarketDataReceived):
        sides = list(PositionSide)
        tasks = [self._process_side(event, side) for side in sides]
        await asyncio.gather(*tasks)

    async def _process_side(self, event, side):
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

        result = await self.ask(
            BatchBars(self.symbol, self.timeframe, cbar, self.max_bars)
        )

        if result.is_err():
            return

        bars = result.unwrap()

        if not bars:
            bars = [event.bar.ohlcv]

        for bar in bars:
            if self._has_anomaly(bar.timestamp, next_risk.time_points):
                logger.debug(f"Anomalous bar skipped: {bar.timestamp}")
                continue

            gap = bar.timestamp - cbar.timestamp

            if gap <= 0:
                logger.debug(f"Stale bar skipped: {bar.timestamp}")
                continue

            if gap > LATENCY_GAP_THRESHOLD * open_signal.timeframe.to_milliseconds():
                logger.debug(f"Latency Gap: {gap} exceeds threshold.")
                continue

            next_risk = next_risk.next(bar)

            if next_risk.has_risk:
                logger.info("Risk threshold breached, triggering position close.")
                await self._close_position(open_signal, side, cbar)
                break

        cbar = next_risk.curr_bar
        next_price = (cbar.high + cbar.low + cbar.close) / 3.0
        pnl = pt.context_factor * (next_price - position.entry_price) * position.size

        ap = performance.next(pnl, position.fee)

        msharpe = ap.modified_sharpe_ratio
        rashev = ap.rachev_ratio
        ir = ap.information_ratio

        logger.info(
            f"{cbar.timestamp}:{open_signal.symbol}:{side} -> "
            f"PnL: {pnl:.4f}, SHARPE: {msharpe:.4f}, IR: {ir:.4f}, RSH: {rashev:.4f}, H: {cbar.high}, L: {cbar.low}, CPR: {next_price:.4f}, TP: {next_risk.tp:.4f}, SL: {next_risk.sl:.4f}"
        )

        next_state = (next_risk, position, pt, performance)

        await self._state.set(side, next_state)

    async def _close_position(self, open_signal, side, bar):
        exit_price = (bar.high + bar.low + bar.close) / 3.0

        close_signal = Signal(
            symbol=open_signal.symbol,
            timeframe=open_signal.timeframe,
            strategy=open_signal.strategy,
            side=open_signal.side,
            ohlcv=bar,
            entry=open_signal.entry,
            exit=exit_price,
        )

        event = (
            RiskLongThresholdBreached(signal=close_signal)
            if side == PositionSide.LONG
            else RiskShortThresholdBreached(signal=close_signal)
        )

        await self.tell(event)

    def _has_anomaly(self, bar_timestamp: float, time_points: list[float]) -> bool:
        if len(time_points) < 3:
            return False

        time_points = np.array(time_points)

        ts_diff = np.diff(np.array(time_points))
        ts_ema = _ema(ts_diff, alpha=0.1)

        mean_diff = np.mean(ts_ema)
        std_diff = np.std(ts_ema)
        threshold = max(std_diff, np.finfo(float).eps)

        current_diff = bar_timestamp - time_points[-1]

        anomaly_score = abs((current_diff - mean_diff) / threshold)
        anomaly_score = np.clip(anomaly_score, -ANOMALY_CLIP, ANOMALY_CLIP)

        if anomaly_score > self.anomaly_threshold:
            self.consc_anomaly_counter += 1
            if self.consc_anomaly_counter > MAX_CONSECUTIVE_ANOMALIES:
                self.anomaly_threshold *= DYNAMIC_THRESHOLD_MULTIPLIER
                self.max_bars *= DYNAMIC_THRESHOLD_MULTIPLIER
                self.consc_anomaly_counter = 0
            return True

        self.anomaly_threshold = DEFAULT_ANOMALY_THRESHOLD
        self.max_bars = DEFAULT_MAX_BARS
        self.consc_anomaly_counter = 0

        return False
