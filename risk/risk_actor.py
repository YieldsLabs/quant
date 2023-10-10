from typing import Union

from core.actors.base import BaseActor
from core.events.ohlcv import NewMarketDataReceived
from core.events.position import PositionClosed, PositionOpened
from core.events.risk import RiskThresholdBreached
from core.models.ohlcv import OHLCV
from core.models.position import Position, PositionSide
from core.models.strategy import Strategy
from core.models.symbol import Symbol
from core.models.timeframe import Timeframe

RiskEvent = Union[NewMarketDataReceived, PositionOpened, PositionClosed]


class RiskActor(BaseActor):
    def __init__(
        self,
        symbol: Symbol,
        timeframe: Timeframe,
        strategy: Strategy,
        risk_buffer: float,
    ):
        super().__init__(symbol, timeframe, strategy)
        self._position = None
        self.risk_buffer = risk_buffer

    async def start(self):
        await super().start()

        self._dispatcher.register(
            NewMarketDataReceived, self.handle, self._market_event_filter
        )

        for event in [PositionOpened, PositionClosed]:
            self._dispatcher.register(event, self.handle, self._position_event_filter)

    async def stop(self):
        await super().stop()

        for event in [NewMarketDataReceived, PositionOpened, PositionClosed]:
            self._dispatcher.unregister(event, self.handle)

    async def handle(self, event: RiskEvent):
        if isinstance(event, NewMarketDataReceived):
            await self.handle_risk(event)
        elif isinstance(event, PositionOpened):
            self._position = event.position
        elif isinstance(event, PositionClosed):
            self._position = None

    async def handle_risk(self, event: NewMarketDataReceived):
        current_position = self._position

        next_position = current_position.next(event.ohlcv)

        if self._should_exit(next_position, event.ohlcv):
            await self._process_exit(current_position, event.ohlcv)

    def _position_event_filter(self, event: PositionOpened):
        signal = event.position.signal
        return self._symbol == signal.symbol and self._timeframe == signal.timeframe

    def _market_event_filter(self, event: NewMarketDataReceived):
        return (
            event.symbol == self._symbol
            and event.timeframe == self._timeframe
            and self._position
        )

    async def _process_exit(self, position, ohlcv):
        exit_price = self._calculate_exit_price(position, ohlcv)

        await self.dispatch(RiskThresholdBreached(position, ohlcv, exit_price))

    def _should_exit(self, next_position: Position, ohlcv: OHLCV):
        if next_position.side == PositionSide.LONG:
            should_exit = self._long_exit_conditions(
                next_position.stop_loss_price,
                next_position.take_profit_price,
                ohlcv.low,
                ohlcv.high,
                self.risk_buffer,
            )
        elif next_position.side == PositionSide.SHORT:
            should_exit = self._short_exit_conditions(
                next_position.stop_loss_price,
                next_position.take_profit_price,
                ohlcv.low,
                ohlcv.high,
                self.risk_buffer,
            )

        return should_exit

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
