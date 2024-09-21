import asyncio
import logging
import time
from typing import Union

from core.actors import StrategyActor
from core.events.meta import EventMeta
from core.events.backtest import BacktestEnded
from core.events.position import (
    BrokerPositionClosed,
    BrokerPositionOpened,
    PositionClosed,
    PositionCloseRequested,
    PositionInitialized,
    PositionOpened,
)
from core.events.risk import RiskThresholdBreached
from core.events.signal import (
    GoLongSignalReceived,
    GoShortSignalReceived,
)
from core.interfaces.abstract_config import AbstractConfig
from core.interfaces.abstract_position_factory import AbstractPositionFactory
from core.models.risk_type import SignalRiskType
from core.models.side import PositionSide
from core.models.symbol import Symbol
from core.models.timeframe import Timeframe
from core.queries.copilot import EvaluateSignal
from core.queries.ohlcv import TA, BackNBars

from ._sm import LONG_TRANSITIONS, SHORT_TRANSITIONS, PositionStateMachine
from ._state import PositionStorage

SignalEvent = Union[GoLongSignalReceived, GoShortSignalReceived]
BrokerPositionEvent = Union[BrokerPositionOpened, BrokerPositionClosed]
ExitSignal = RiskThresholdBreached
BacktestSignal = BacktestEnded

PositionEvent = Union[SignalEvent, ExitSignal, BrokerPositionEvent, BacktestSignal]

logger = logging.getLogger(__name__)

TIME_BUFF = 3
N_BACK_BARS = 4


class PositionActor(StrategyActor):
    def __init__(
        self,
        symbol: Symbol,
        timeframe: Timeframe,
        position_factory: AbstractPositionFactory,
        config_service: AbstractConfig,
    ):
        super().__init__(symbol, timeframe)
        self.position_factory = position_factory

        self.long_sm = PositionStateMachine(self, LONG_TRANSITIONS)
        self.short_sm = PositionStateMachine(self, SHORT_TRANSITIONS)
        self.state = PositionStorage()
        self.config = config_service.get("position")

    async def on_receive(self, event: PositionEvent):
        symbol, _ = self._get_event_key(event)

        if hasattr(event, "position"):
            if event.position.side == PositionSide.LONG:
                await self.long_sm.process_event(symbol, event)
            if event.position.side == PositionSide.SHORT:
                await self.short_sm.process_event(symbol, event)
        else:
            await asyncio.gather(
                *[
                    self.long_sm.process_event(symbol, event),
                    self.short_sm.process_event(symbol, event),
                ]
            )

    async def handle_signal_received(self, event: SignalEvent) -> bool:
        if self._is_stale_signal(event.meta):
            logger.warn(f"Stale Signal: {event}, {time.time()}")
            return False

        async def create_and_store_position(event: SignalEvent):
            symbol, timeframe, ohlcv = (
                event.signal.symbol,
                event.signal.timeframe,
                event.signal.ohlcv,
            )

            back_bars = await self.ask(BackNBars(symbol, timeframe, ohlcv, N_BACK_BARS))
            ta = await self.ask(TA(symbol, timeframe, ohlcv))
            signal_risk_level = await self.ask(
                EvaluateSignal(event.signal, back_bars, ta)
            )

            if signal_risk_level.type in {
                SignalRiskType.UNKNOWN,
                SignalRiskType.VERY_HIGH,
            }:
                return False

            position = await self.position_factory.create(
                event.signal, signal_risk_level, ta
            )

            await self.state.store_position(position)
            await self.tell(PositionInitialized(position))
            return True

        symbol, timeframe = self._get_event_key(event)
        long_position, short_position = await self.state.retrieve_position(
            symbol, timeframe
        )

        if not long_position and isinstance(event, GoLongSignalReceived):
            return await create_and_store_position(event)

        if not short_position and isinstance(event, GoShortSignalReceived):
            return await create_and_store_position(event)

        return False

    async def handle_position_opened(self, event: BrokerPositionOpened) -> bool:
        symbol, timeframe = self._get_event_key(event)
        long_position, short_position = await self.state.retrieve_position(
            symbol, timeframe
        )

        if (
            event.position.side == PositionSide.LONG
            and long_position
            and long_position.last_modified < event.meta.timestamp
        ) or (
            event.position.side == PositionSide.SHORT
            and short_position
            and short_position.last_modified < event.meta.timestamp
        ):
            next_position = await self.state.update_stored_position(event.position)
            await self.tell(PositionOpened(next_position))
            return True

        return False

    async def handle_position_closed(self, event: BrokerPositionClosed) -> bool:
        symbol, timeframe = self._get_event_key(event)
        long_position, short_position = await self.state.retrieve_position(
            symbol, timeframe
        )

        if (event.position.side == PositionSide.LONG and long_position) or (
            event.position.side == PositionSide.SHORT and short_position
        ):
            await self.state.close_stored_position(event.position)
            await self.tell(PositionClosed(event.position))
            return True

        return False

    async def handle_exit_received(self, event: ExitSignal) -> bool:
        if not event.position.has_risk:
            logger.warn(f"Attempt to close not risky position: {event.position}")

        symbol, timeframe = self._get_event_key(event)
        long_position, short_position = await self.state.retrieve_position(
            symbol, timeframe
        )

        if (
            event.position.side == PositionSide.LONG
            and long_position
            and long_position.last_modified < event.meta.timestamp
        ) or (
            event.position.side == PositionSide.SHORT
            and short_position
            and short_position.last_modified < event.meta.timestamp
        ):
            next_position = await self.state.update_stored_position(event.position)
            await self.tell(PositionCloseRequested(next_position))
            return True

        return False

    async def handle_backtest(self, event: BacktestSignal) -> bool:
        symbol, timeframe = self._get_event_key(event)
        long_position, short_position = await self.state.retrieve_position(
            symbol, timeframe
        )

        if long_position:
            await self.tell(PositionCloseRequested(long_position))

        if short_position:
            await self.tell(PositionCloseRequested(short_position))

        return True

    @staticmethod
    def _is_stale_signal(meta: EventMeta) -> bool:
        return int(meta.timestamp) < int(time.time()) - TIME_BUFF

    @staticmethod
    def _get_event_key(event: PositionEvent):
        signal = (
            event.signal
            if hasattr(event, "signal")
            else event.position.signal
            if hasattr(event, "position")
            else event
        )

        return (signal.symbol, signal.timeframe)
