import asyncio
from typing import Union

from core.events.ohlcv import NewMarketDataReceived
from core.events.position import PositionClosed, PositionOpened
from core.interfaces.abstract_actor import AbstractActor
from core.models.ohlcv import OHLCV
from core.events.risk import RiskThresholdBreached
from core.models.position import Position, PositionSide
from core.models.symbol import Symbol
from core.models.timeframe import Timeframe

RiskEvent = Union[NewMarketDataReceived, PositionOpened, PositionClosed]

class RiskActor(AbstractActor):
    def __init__(self, 
                symbol: Symbol,
                timeframe: Timeframe,
                risk_buffer: float,
        ):
        super().__init__()
        self._symbol = symbol
        self._timeframe = timeframe
        self._position = None
        self._lock = asyncio.Lock()
        self._running = False
        self.risk_buffer = risk_buffer

    @property
    def id(self):
        return f"{self._symbol}_{self._timeframe}"

    @property
    async def running(self):
        async with self._lock:
            return self._running 
    
    async def start(self):
        if await self.running:
            raise RuntimeError("Start: risk is running")

        async with self._lock:
            self._running = True

        self._dispatcher.register(NewMarketDataReceived, self._market_event_filter)
        self._dispatcher.register(PositionOpened, self._position_event_filter)
        self._dispatcher.register(PositionClosed, self._position_event_filter)

    async def stop(self):
        if not await self.running:
            raise RuntimeError("Stop: risk is not started")
        
        async with self._lock:
            self._running = False

        self._dispatcher.unregister(NewMarketDataReceived, self._market_event_filter)
        self._dispatcher.unregister(PositionOpened, self._position_event_filter)
        self._dispatcher.unregister(PositionClosed, self._position_event_filter)
    
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

    async def _position_event_filter(self, event: PositionOpened):
        signal = event.position.signal
    
        if self._symbol == signal.symbol and self._timeframe == signal.timeframe:
            await self.handle(event)

    async def _market_event_filter(self, event: NewMarketDataReceived):
        if event.symbol == self._symbol and event.timeframe == self._timeframe and self._position:
            await self.handle(event)

    async def _process_exit(self, position, ohlcv):
        exit_price = self._calculate_exit_price(position, ohlcv)

        await self.dispatch(RiskThresholdBreached(position, exit_price))

    def _should_exit(self, next_position: Position, ohlcv: OHLCV):
        if next_position.side == PositionSide.LONG:
            should_exit = self._long_exit_conditions(next_position.stop_loss_price, next_position.take_profit_price, ohlcv.low, ohlcv.high, self.risk_buffer)
        elif next_position.side == PositionSide.SHORT:
            should_exit = self._short_exit_conditions(next_position.stop_loss_price, next_position.take_profit_price, ohlcv.low, ohlcv.high, self.risk_buffer)

        return should_exit

    @staticmethod
    def _calculate_exit_price(position: Position, ohlcv: OHLCV):
        if position.side == PositionSide.LONG:
            current_close = ohlcv.high
            exit_price = max(min(current_close, position.take_profit_price or current_close),
                             position.stop_loss_price or current_close)
        elif position.side == PositionSide.SHORT:
            current_close = ohlcv.low
            exit_price = min(max(current_close, position.take_profit_price or current_close),
                             position.stop_loss_price or current_close)
        return exit_price

    @staticmethod
    def _long_exit_conditions(stop_loss_price: float | None, take_profit_price: float | None, low: float, high: float, risk_buffer: float):
        return (stop_loss_price is not None and low <= stop_loss_price * (1 - risk_buffer)) or \
               (take_profit_price is not None and high >= take_profit_price * (1 + risk_buffer))

    @staticmethod
    def _short_exit_conditions(stop_loss_price: float | None, take_profit_price: float | None, low: float, high: float, risk_buffer: float):
        return (stop_loss_price is not None and high >= stop_loss_price * (1 + risk_buffer)) or \
               (take_profit_price is not None and low <= take_profit_price * (1 - risk_buffer))
