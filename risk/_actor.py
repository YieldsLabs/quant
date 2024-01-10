import asyncio
from typing import Optional, Union

from core.actors import Actor
from core.events.ohlcv import NewMarketDataReceived
from core.events.position import PositionClosed, PositionOpened
from core.events.risk import RiskThresholdBreached
from core.events.signal import (
    ExitLongSignalReceived,
    ExitShortSignalReceived,
    GoLongSignalReceived,
    GoShortSignalReceived,
)
from core.interfaces.abstract_config import AbstractConfig
from core.models.ohlcv import OHLCV
from core.models.position import Position, PositionSide
from core.models.strategy import Strategy
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
        strategy: Strategy,
        config_service: AbstractConfig,
    ):
        super().__init__(symbol, timeframe, strategy)
        self.lock = asyncio.Lock()
        self._position = (None, None)

        self.config = config_service.get("position")

    def pre_receive(self, event: RiskEvent):
        long_position, short_position = self._position

        if isinstance(event, NewMarketDataReceived) and (
            not long_position and not short_position
        ):
            return False

        symbol, timeframe = self._get_event_key(event)
        return self._symbol == symbol and self._timeframe == timeframe

    async def on_receive(self, event: RiskEvent):
        handlers = {
            NewMarketDataReceived: self._handle_market_risk,
            PositionOpened: self._update_position,
            PositionClosed: self._close_position,
            GoLongSignalReceived: self._handle_reverse_exit,
            GoShortSignalReceived: self._handle_reverse_exit,
            ExitLongSignalReceived: self._handle_signal_exit,
            ExitShortSignalReceived: self._handle_signal_exit,
        }

        handler = handlers.get(type(event))

        if handler:
            await handler(event)

    async def _update_position(self, event: PositionOpened):
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
            current_long_position, current_short_position = self._position

            self._position = await asyncio.gather(
                *[
                    self._process_position(event.ohlcv, current_long_position),
                    self._process_position(event.ohlcv, current_short_position),
                ]
            )

    async def _handle_reverse_exit(
        self, event: Union[GoLongSignalReceived, GoShortSignalReceived]
    ):
        async with self.lock:
            long_position, short_position = self._position

            if long_position and isinstance(event, GoShortSignalReceived):
                long_position = await self._process_close(
                    long_position,
                    event.entry_price,
                    self.config["tp_threshold"],
                    self.config["sl_threshold"],
                )

            if short_position and isinstance(event, GoLongSignalReceived):
                short_position = await self._process_close(
                    short_position,
                    event.entry_price,
                    self.config["tp_threshold"],
                    self.config["sl_threshold"],
                )

            self._position = (long_position, short_position)

    async def _handle_signal_exit(
        self, event: Union[ExitLongSignalReceived, ExitShortSignalReceived]
    ):
        async with self.lock:
            long_position, short_position = self._position

            if long_position and isinstance(event, ExitLongSignalReceived):
                long_position = await self._process_close(
                    long_position,
                    event.exit_price,
                    self.config["tp_threshold"],
                    self.config["sl_threshold"],
                )

            if short_position and isinstance(event, ExitShortSignalReceived):
                short_position = await self._process_close(
                    short_position,
                    event.exit_price,
                    self.config["tp_threshold"],
                    self.config["sl_threshold"],
                )

            self._position = (long_position, short_position)

    async def _process_position(self, ohlcv: OHLCV, position: Optional[Position]):
        next_position = None

        if position:
            next_position = position.next(ohlcv)

            if self._should_exit(next_position, ohlcv):
                await self._process_exit(position, ohlcv)
                return None

        return next_position

    async def _process_exit(self, position, ohlcv):
        exit_price = self._calculate_exit_price(position, ohlcv)

        await self.tell(RiskThresholdBreached(position, exit_price))

    def _should_exit(self, next_position: Position, ohlcv: OHLCV):
        expiration = (
            next_position.open_timestamp + self.config["trade_duration"] * 1000
        ) - ohlcv.timestamp

        if next_position.side == PositionSide.LONG:
            return self._check_long_exit(next_position, expiration, ohlcv)
        elif next_position.side == PositionSide.SHORT:
            return self._check_short_exit(next_position, expiration, ohlcv)

        return False

    def _check_long_exit(
        self, next_position: Position, expiration: int, ohlcv: OHLCV
    ) -> bool:
        if expiration <= 0 and next_position.entry_price < min(ohlcv.close, ohlcv.low):
            return True
        else:
            return self._long_exit_conditions(
                next_position.stop_loss_price,
                next_position.take_profit_price,
                ohlcv.low,
                ohlcv.high,
                self.config["risk_buffer"],
            )

    def _check_short_exit(
        self, next_position: Position, expiration: int, ohlcv: OHLCV
    ) -> bool:
        if expiration <= 0 and next_position.entry_price > max(ohlcv.close, ohlcv.high):
            return True
        else:
            return self._short_exit_conditions(
                next_position.stop_loss_price,
                next_position.take_profit_price,
                ohlcv.low,
                ohlcv.high,
                self.config["risk_buffer"],
            )

    @staticmethod
    def _calculate_exit_price(position: Position, ohlcv: OHLCV):
        if position.side == PositionSide.LONG:
            if (
                position.stop_loss_price is not None
                and ohlcv.low <= position.stop_loss_price
            ):
                return position.stop_loss_price
            if (
                position.take_profit_price is not None
                and ohlcv.high >= position.take_profit_price
            ):
                return position.take_profit_price

            return ohlcv.close

        elif position.side == PositionSide.SHORT:
            if (
                position.stop_loss_price is not None
                and ohlcv.high >= position.stop_loss_price
            ):
                return position.stop_loss_price
            if (
                position.take_profit_price is not None
                and ohlcv.low <= position.take_profit_price
            ):
                return position.take_profit_price

            return ohlcv.close

    @staticmethod
    def _long_exit_conditions(
        stop_loss_price: float | None,
        take_profit_price: float | None,
        low: float,
        high: float,
        risk_buffer: float,
    ):
        return (
            stop_loss_price is not None and low <= stop_loss_price * (1 - risk_buffer)
        ) or (
            take_profit_price is not None
            and high >= take_profit_price * (1 + risk_buffer)
        )

    @staticmethod
    def _short_exit_conditions(
        stop_loss_price: float | None,
        take_profit_price: float | None,
        low: float,
        high: float,
        risk_buffer: float,
    ):
        return (
            stop_loss_price is not None and high >= stop_loss_price * (1 + risk_buffer)
        ) or (
            take_profit_price is not None
            and low <= take_profit_price * (1 - risk_buffer)
        )

    async def _process_close(
        self,
        position: Position,
        price: float,
        tp_threshold: float,
        sl_threshold: float,
    ):
        side = position.side
        take_profit_price = position.take_profit_price
        stop_loss_price = position.stop_loss_price

        price_exceeds_take_profit = (
            side == PositionSide.LONG and price >= take_profit_price
        ) or (side == PositionSide.SHORT and price <= take_profit_price)

        price_exceeds_stop_loss = (
            side == PositionSide.LONG and price <= stop_loss_price
        ) or (side == PositionSide.SHORT and price >= stop_loss_price)

        if price_exceeds_take_profit or price_exceeds_stop_loss:
            print("XXXXX")
            await self.tell(RiskThresholdBreached(position, price))
            return None

        diff_to_stop_loss = abs((price - stop_loss_price) / stop_loss_price) * 100
        diff_to_take_profit = abs((price - take_profit_price) / take_profit_price) * 100

        if diff_to_take_profit <= tp_threshold or diff_to_stop_loss <= sl_threshold:
            print("Closssssseee")
            await self.tell(RiskThresholdBreached(position, price))
            return None

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
