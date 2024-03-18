import asyncio
from collections import deque
from typing import List, Optional, Tuple, Union

from core.actors import Actor
from core.events.ohlcv import NewMarketDataReceived
from core.events.position import PositionClosed, PositionOpened
from core.events.risk import RiskThresholdBreached, RiskType
from core.events.signal import (
    ExitLongSignalReceived,
    ExitShortSignalReceived,
    GoLongSignalReceived,
    GoShortSignalReceived,
)
from core.interfaces.abstract_config import AbstractConfig
from core.models.ohlcv import OHLCV
from core.models.position import Position
from core.models.position_side import PositionSide
from core.models.symbol import Symbol
from core.models.timeframe import Timeframe

RiskEvent = Union[
    NewMarketDataReceived,
    PositionOpened,
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
        ExitLongSignalReceived,
        ExitShortSignalReceived,
        GoLongSignalReceived,
        GoShortSignalReceived,
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
        self._ohlcv = deque(maxlen=233)
        self.config = config_service.get("position")

    def pre_receive(self, event: RiskEvent):
        symbol, timeframe = self._get_event_key(event)
        return self._symbol == symbol and self._timeframe == timeframe

    async def on_receive(self, event: RiskEvent):
        handlers = {
            NewMarketDataReceived: self._handle_market_risk,
            PositionOpened: self._open_position,
            PositionClosed: self._close_position,
            GoLongSignalReceived: self._handle_reverse_exit,
            GoShortSignalReceived: self._handle_reverse_exit,
            ExitLongSignalReceived: self._handle_signal_exit,
            ExitShortSignalReceived: self._handle_signal_exit,
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

            if not long_position and not short_position:
                self._ohlcv.clear()

    async def _handle_market_risk(self, event: NewMarketDataReceived):
        async with self.lock:
            self._ohlcv.append(event.ohlcv)

            current_long_position, current_short_position = self._position

            ohlcvs = list(self._ohlcv)

            self._position = await asyncio.gather(
                *[
                    self._process_position(current_long_position, ohlcvs),
                    self._process_position(current_short_position, ohlcvs),
                ]
            )

    async def _handle_reverse_exit(
        self, event: Union[GoLongSignalReceived, GoShortSignalReceived]
    ):
        async with self.lock:
            long_position, short_position = self._position

            if (
                long_position
                and not short_position
                and isinstance(event, GoShortSignalReceived)
            ):
                long_position = await self._process_signal_exit(
                    long_position,
                    event.entry_price,
                )

            if (
                short_position
                and not long_position
                and isinstance(event, GoLongSignalReceived)
            ):
                short_position = await self._process_signal_exit(
                    short_position,
                    event.entry_price,
                )

            self._position = (long_position, short_position)

    async def _handle_signal_exit(
        self, event: Union[ExitLongSignalReceived, ExitShortSignalReceived]
    ):
        async with self.lock:
            long_position, short_position = self._position

            if long_position and isinstance(event, ExitLongSignalReceived):
                long_position = await self._process_signal_exit(
                    long_position,
                    event.exit_price,
                )

            if short_position and isinstance(event, ExitShortSignalReceived):
                short_position = await self._process_signal_exit(
                    short_position,
                    event.exit_price,
                )

            self._position = (long_position, short_position)

    async def _process_position(
        self, position: Optional[Position], ohlcvs: List[Tuple[OHLCV, bool]]
    ):
        next_position = position

        if position and len(ohlcvs) > 1:
            next_position = position.next(ohlcvs)
            last_candle = ohlcvs[-1]

            exit_event = self._create_exit_event(next_position, last_candle)

            if exit_event:
                await self.tell(exit_event)
                return None

        return next_position

    def _create_exit_event(self, position: Position, ohlcv: OHLCV):
        expiration = (
            position.open_timestamp + self.config["trade_duration"] * 1000
        ) - ohlcv.timestamp

        risk_type = None

        if position.side == PositionSide.LONG:
            if self._is_long_expires(position, expiration, ohlcv):
                risk_type = RiskType.TIME
            elif self._is_long_meets_tp(position, ohlcv):
                risk_type = RiskType.TP
            elif self._is_long_meets_sl(position, ohlcv):
                risk_type = RiskType.SL
        elif position.side == PositionSide.SHORT:
            if self._is_short_expires(position, expiration, ohlcv):
                risk_type = RiskType.TIME
            elif self._is_short_meets_tp(position, ohlcv):
                risk_type = RiskType.TP
            elif self._is_short_meets_sl(position, ohlcv):
                risk_type = RiskType.SL

        if risk_type:
            exit_price = (
                self._long_exit_price
                if position.side == PositionSide.LONG
                else self._short_exit_price
            )(position, ohlcv)

            return RiskThresholdBreached(position, exit_price, risk_type)

        return None

    async def _process_signal_exit(
        self,
        position: Position,
        price: float,
    ):
        side = position.side
        take_profit_price = position.take_profit_price
        stop_loss_price = position.stop_loss_price

        price_exceeds_take_profit = (
            side == PositionSide.LONG and price > take_profit_price
        ) or (side == PositionSide.SHORT and price < take_profit_price)

        price_exceeds_stop_loss = (
            side == PositionSide.LONG and price < stop_loss_price
        ) or (side == PositionSide.SHORT and price > stop_loss_price)

        if price_exceeds_take_profit or price_exceeds_stop_loss:
            return position

        distance_to_take_profit = abs(price - take_profit_price)
        distance_to_stop_loss = abs(price - stop_loss_price)

        if distance_to_take_profit < distance_to_stop_loss and (
            (side == PositionSide.LONG and price > position.entry_price)
            or (side == PositionSide.SHORT and price < position.entry_price)
        ):
            await self.tell(RiskThresholdBreached(position, price, RiskType.SIGNAL))
            return None

        return position

    @staticmethod
    def _long_exit_price(position: Position, ohlcv: OHLCV):
        if (
            position.stop_loss_price is not None
            and ohlcv.low <= position.stop_loss_price
        ):
            return ohlcv.low
        if (
            position.take_profit_price is not None
            and ohlcv.high >= position.take_profit_price
        ):
            return ohlcv.high

        return ohlcv.close

    @staticmethod
    def _is_long_expires(
        position: Position,
        expiration: int,
        ohlcv: OHLCV,
    ) -> bool:
        return (
            expiration <= 0
            and position.entry_price > max(ohlcv.close, ohlcv.high) * 1.1
        )

    @staticmethod
    def _is_long_meets_tp(
        position: Position,
        ohlcv: OHLCV,
    ):
        return (
            position.take_profit_price is not None
            and ohlcv.high > position.take_profit_price
        )

    @staticmethod
    def _is_long_meets_sl(
        position: Position,
        ohlcv: OHLCV,
    ):
        return (
            position.stop_loss_price is not None
            and ohlcv.low < position.stop_loss_price
        )

    @staticmethod
    def _short_exit_price(position: Position, ohlcv: OHLCV):
        if (
            position.stop_loss_price is not None
            and ohlcv.high >= position.stop_loss_price
        ):
            return ohlcv.high
        if (
            position.take_profit_price is not None
            and ohlcv.low <= position.take_profit_price
        ):
            return ohlcv.low

        return ohlcv.close

    @staticmethod
    def _is_short_expires(
        position: Position,
        expiration: int,
        ohlcv: OHLCV,
    ) -> bool:
        return expiration <= 0 and position.entry_price * 1.1 < min(
            ohlcv.close, ohlcv.low
        )

    @staticmethod
    def _is_short_meets_tp(
        position: Position,
        ohlcv: OHLCV,
    ):
        return (
            position.take_profit_price is not None
            and ohlcv.low < position.take_profit_price
        )

    @staticmethod
    def _is_short_meets_sl(
        position: Position,
        ohlcv: OHLCV,
    ):
        return (
            position.stop_loss_price is not None
            and ohlcv.high > position.stop_loss_price
        )

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
