import asyncio
import logging
import time
from typing import Optional, Union

from core.actors import StrategyActor
from core.events.backtest import BacktestEnded
from core.events.meta import EventMeta
from core.events.position import (
    BrokerPositionClosed,
    BrokerPositionOpened,
    PositionClosed,
    PositionCloseRequested,
    PositionInitialized,
    PositionOpened,
)
from core.events.risk import (
    RiskLongThresholdBreached,
    RiskShortThresholdBreached,
)
from core.events.signal import (
    GoLongSignalReceived,
    GoShortSignalReceived,
)
from core.models.entity.position import Position
from core.models.entity.signal import Signal
from core.models.side import PositionSide
from core.models.symbol import Symbol
from core.models.timeframe import Timeframe
from core.queries.portfolio import GetPortfolioPerformance

from ._sm import LONG_TRANSITIONS, SHORT_TRANSITIONS, PositionStateMachine
from ._state import PositionStorage

SignalEvent = Union[GoLongSignalReceived, GoShortSignalReceived]
BrokerPositionEvent = Union[BrokerPositionOpened, BrokerPositionClosed]
ExitSignal = Union[RiskLongThresholdBreached, RiskShortThresholdBreached]
BacktestSignal = BacktestEnded

PositionEvent = Union[SignalEvent, ExitSignal, BrokerPositionEvent, BacktestSignal]

logger = logging.getLogger(__name__)

TIME_BUFF = 3


class PositionActor(StrategyActor):
    def __init__(
        self,
        symbol: Symbol,
        timeframe: Timeframe,
    ):
        super().__init__(symbol, timeframe)
        self.long_sm = PositionStateMachine(self, LONG_TRANSITIONS)
        self.short_sm = PositionStateMachine(self, SHORT_TRANSITIONS)
        self.state = PositionStorage()

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
            performance = await self.ask(
                GetPortfolioPerformance(
                    self.symbol, self.timeframe, event.signal.strategy
                )
            )

            initial_size = performance.equity[-1] * performance.risk_per_trade
            initial_size = max(initial_size, self.symbol.min_position_size)

            logger.info(f"Initial Size: {initial_size}")

            position = Position(initial_size=initial_size)
            position = position.open_position(event.signal)

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
        async def close_position(
            event: ExitSignal, position: Optional[Position]
        ) -> bool:
            if position and position.last_modified < event.meta.timestamp:
                closed_position = position.close_position(event.signal)
                closed_position = await self.state.update_stored_position(
                    closed_position
                )
                await self.tell(PositionCloseRequested(closed_position))
                return True

            return False

        symbol, timeframe = self._get_event_key(event)
        long_position, short_position = await self.state.retrieve_position(
            symbol, timeframe
        )

        if isinstance(event, RiskLongThresholdBreached):
            return await close_position(event, long_position)

        if isinstance(event, RiskShortThresholdBreached):
            return await close_position(event, short_position)

        return False

    async def handle_backtest(self, event: BacktestSignal) -> bool:
        symbol, timeframe = self._get_event_key(event)
        long_position, short_position = await self.state.retrieve_position(
            symbol, timeframe
        )

        if long_position:
            open_signal = long_position.signal
            close_signal = Signal(
                symbol=open_signal.symbol,
                timeframe=open_signal.timeframe,
                strategy=open_signal.strategy,
                side=open_signal.side,
                ohlcv=open_signal.ohlcv,
                entry=open_signal.entry,
                exit=open_signal.entry,
            )
            position = long_position.close_position(close_signal)
            await self.tell(PositionCloseRequested(position))

        if short_position:
            open_signal = short_position.signal
            close_signal = Signal(
                symbol=open_signal.symbol,
                timeframe=open_signal.timeframe,
                strategy=open_signal.strategy,
                side=open_signal.side,
                ohlcv=open_signal.ohlcv,
                entry=open_signal.entry,
                exit=open_signal.entry,
            )
            position = short_position.close_position(close_signal)
            await self.tell(PositionCloseRequested(position))

        return True

    @staticmethod
    def _is_stale_signal(meta: EventMeta) -> bool:
        return int(meta.timestamp) < int(time.time()) - TIME_BUFF

    @staticmethod
    def _get_event_key(event: PositionEvent):
        signal = (
            event.signal
            if hasattr(event, "signal")
            else event.position.signal if hasattr(event, "position") else event
        )

        return (signal.symbol, signal.timeframe)
