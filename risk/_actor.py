import asyncio
from collections import deque
from typing import List, Optional, Union

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
from core.models.ohlcv import OHLCV
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


class RiskActor(Actor):
    _EVENTS = [
        NewMarketDataReceived,
        PositionOpened,
        PositionClosed,
        # ExitLongSignalReceived,
        # ExitShortSignalReceived,
        # GoLongSignalReceived,
        # GoShortSignalReceived,
    ]

    def __init__(
        self,
        symbol: Symbol,
        timeframe: Timeframe,
        config_service: AbstractConfig,
    ):
        super().__init__(symbol, timeframe)
        self.lock = asyncio.Lock()
        self._position = (None, None)
        self._ohlcv = deque(maxlen=120)
        self.config = config_service.get("position")

    def pre_receive(self, event: RiskEvent):
        symbol, timeframe = self._get_event_key(event)
        return self._symbol == symbol and self._timeframe == timeframe

    async def on_receive(self, event: RiskEvent):
        handlers = {
            NewMarketDataReceived: self._handle_market_risk,
            PositionOpened: self._open_position,
            PositionClosed: self._close_position,
        }

        handler = handlers.get(type(event))

        if handler:
            await handler(event)

    async def _open_position(self, event: PositionOpened):
        async with self.lock:
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
        async with self.lock:
            long_position, short_position = self._position

            self._position = (
                None if event.position.side == PositionSide.LONG else long_position,
                None if event.position.side == PositionSide.SHORT else short_position,
            )

    async def _handle_market_risk(self, event: NewMarketDataReceived):
        async with self.lock:
            self._ohlcv.append(event.ohlcv)
            visited = set()
            ohlcvs = []

            for i in range(len(self._ohlcv)):
                if self._ohlcv[i].timestamp not in visited:
                    ohlcvs.append(self._ohlcv[i])
                    visited.add(self._ohlcv[i].timestamp)

            ohlcvs = sorted(ohlcvs, key=lambda x: x.timestamp)

            long_position, short_position = self._position

            if long_position or short_position:
                long_position, short_position = await asyncio.gather(
                    *[
                        self._process_market(long_position, ohlcvs),
                        self._process_market(short_position, ohlcvs),
                    ]
                )

                self._position = (long_position, short_position)

    # async def _handle_signal_exit(
    #     self, event: Union[ExitLongSignalReceived, ExitShortSignalReceived]
    # ):
    #     async with self.lock:
    #         long_position, short_position = self._position

    #         if isinstance(event, ExitLongSignalReceived) and long_position:
    #             await self._process_signal_exit(
    #                 long_position,
    #                 event.signal.exit,
    #             )
    #         if isinstance(event, ExitShortSignalReceived) and short_position:
    #             await self._process_signal_exit(
    #                 short_position,
    #                 event.signal.exit,
    #             )

    async def _process_market(self, position: Optional[Position], ohlcvs: List[OHLCV]):
        next_position = position

        if position and len(ohlcvs) > 1:
            next_position = position.next(ohlcvs)

            if next_position.has_risk:
                await self.tell(RiskThresholdBreached(next_position))

        return next_position

    async def _process_signal_exit(
        self,
        position: Position,
        price: float,
    ):
        side = position.side
        take_profit_price = position.take_profit
        stop_loss_price = position.stop_loss
        entry_price = position.entry_price

        price_exceeds_take_profit = (
            side == PositionSide.LONG and price > take_profit_price
        ) or (side == PositionSide.SHORT and price < take_profit_price)

        price_exceeds_stop_loss = (
            side == PositionSide.LONG and price < stop_loss_price
        ) or (side == PositionSide.SHORT and price > stop_loss_price)

        if price_exceeds_take_profit or price_exceeds_stop_loss:
            return

        distance_to_take_profit = abs(price - take_profit_price)
        distance_to_stop_loss = abs(price - stop_loss_price)

        trailing_dist = abs(price - entry_price)

        ttp = distance_to_take_profit * self.config["trl_factor"]

        if distance_to_take_profit < distance_to_stop_loss and trailing_dist > ttp:
            await self.tell(RiskThresholdBreached(position))
            return position

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
