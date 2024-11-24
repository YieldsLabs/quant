import asyncio
import logging
import time
from typing import Union

from core.actors import StrategyActor
from core.actors.state import InMemory
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

from ._sm import TRANSITIONS, PositionStateMachine, SMKey

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
        self.sm = PositionStateMachine(self, TRANSITIONS)
        self._state = InMemory[PositionSide, Position]()

    async def on_receive(self, event: PositionEvent):
        if hasattr(event, "position"):
            await self.sm.process_event(event, event.position.side)
        else:
            await asyncio.gather(
                *[
                    self.sm.process_event(event, PositionSide.LONG),
                    self.sm.process_event(event, PositionSide.SHORT),
                ]
            )

    async def handle_signal_received(self, event: SignalEvent) -> bool:
        if self._is_stale_signal(event.meta):
            logger.warn(f"Stale Signal: {event}, {time.time()}")
            return False

        async def create_and_store_position(event: SignalEvent, side: PositionSide):
            key = self._get_key(side)

            if await self._state.exists(key):
                return False

            result = await self.ask(
                GetPortfolioPerformance(
                    self.symbol, self.timeframe, event.signal.strategy
                )
            )

            if result.is_err():
                return False

            performance = result.unwrap()

            initial_size = performance.equity[-1] * performance.risk_per_trade
            initial_size = max(initial_size, self.symbol.min_position_size)

            logger.info(f"Initial Size: {initial_size}")

            position = Position(initial_size=initial_size)
            position = position.open_position(event.signal)

            await self._state.set(key, position)
            await self.tell(PositionInitialized(position))
            return True

        if isinstance(event, GoLongSignalReceived):
            return await create_and_store_position(event, PositionSide.LONG)

        if isinstance(event, GoShortSignalReceived):
            return await create_and_store_position(event, PositionSide.SHORT)

        return False

    async def handle_position_opened(self, event: BrokerPositionOpened) -> bool:
        key = self._get_key(event.position.side)

        position = await self._state.get(key)

        if position and position.last_modified < event.meta.timestamp:
            await self._state.set(key, event.position)
            await self.tell(PositionOpened(event.position))
            return True

        return False

    async def handle_position_closed(self, event: BrokerPositionClosed) -> bool:
        key = self._get_key(event.position.side)

        if await self._state.exists(key):
            await self._state.delete(key)
            await self.tell(PositionClosed(event.position))
            return True

        return False

    async def handle_exit_received(self, event: ExitSignal) -> bool:
        async def close_position(
            event: ExitSignal,
            side: PositionSide,
        ) -> bool:
            key = self._get_key(side)
            position = await self._state.get(key)

            if position and position.last_modified < event.meta.timestamp:
                closed_position = position.close_position(event.signal)

                await self._state.set(key, closed_position)
                await self.tell(PositionCloseRequested(closed_position))
                return True

            return False

        if isinstance(event, RiskLongThresholdBreached):
            return await close_position(event, PositionSide.LONG)

        if isinstance(event, RiskShortThresholdBreached):
            return await close_position(event, PositionSide.SHORT)

        return False

    async def handle_backtest(self, _event: BacktestSignal) -> bool:
        await asyncio.gather(
            self._process_backtest_close(PositionSide.LONG),
            self._process_backtest_close(PositionSide.SHORT),
        )
        return True

    async def _process_backtest_close(self, side: PositionSide):
        key = self._get_key(side)
        position = await self._state.get(key)

        if position:
            open_signal = position.signal
            close_signal = Signal(
                symbol=open_signal.symbol,
                timeframe=open_signal.timeframe,
                strategy=open_signal.strategy,
                side=open_signal.side,
                ohlcv=open_signal.ohlcv,
                entry=open_signal.entry,
                exit=open_signal.entry,
            )

            closed_position = position.close_position(close_signal)
            await self._state.set(key, closed_position)
            await self.tell(PositionCloseRequested(closed_position))

    @staticmethod
    def _is_stale_signal(meta: EventMeta) -> bool:
        return int(meta.timestamp) < int(time.time()) - TIME_BUFF

    def _get_key(self, side: PositionSide) -> SMKey:
        return self.symbol, self.timeframe, side
