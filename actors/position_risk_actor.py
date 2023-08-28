import asyncio

from core.events.ohlcv import NewMarketDataReceived
from core.interfaces.abstract_actor import AbstractActor
from core.models.ohlcv import OHLCV
from core.events.risk import RiskThresholdBreached
from core.models.position import Position, PositionSide


class PositionRiskActor(AbstractActor):
    def __init__(self, 
                position: Position,
                risk_buffer: float,
                event_cooldown: float
        ):
        super().__init__()
        self._lock = asyncio.Lock()
        self._running = False
        self._position = position
        self.last_event_time = None
        self.risk_buffer = risk_buffer
        self.event_cooldown = event_cooldown

    @property
    async def running(self):
        async with self._lock:
            return self._running 
    
    async def start(self):
        if await self.running:
            raise RuntimeError("Start: risk is running")

        async with self._lock:
            self._running = True

        self.last_event_time = None
        self.dispatcher.register(NewMarketDataReceived, self._position_event_filter)

    async def stop(self):
        if not await self.running:
            raise RuntimeError("Stop: risk is not started")
        
        async with self._lock:
            self._running = False

        self.last_event_time = None
        self.dispatcher.unregister(NewMarketDataReceived, self._position_event_filter)
    
    async def next(self, event: NewMarketDataReceived):
        current_position = self._position
        
        next_position = current_position.next(event.ohlcv)

        if self._should_exit(next_position, event.ohlcv):
            await self._process_exit(current_position, event.ohlcv)
        else:
            self._position = next_position

    async def _position_event_filter(self, event: NewMarketDataReceived):
        if event.symbol == self._position.signal.symbol and event.timeframe == self._position.signal.timeframe:
            await self.next(event)

    async def _process_exit(self, position, ohlcv):
        exit_price = self._calculate_exit_price(position, ohlcv)

        await self.dispatcher.dispatch(RiskThresholdBreached(position.signal, position.side, exit_price))

    def _should_exit(self, next_position: Position, ohlcv: OHLCV):
        current_time = asyncio.get_event_loop().time()
        
        if self.last_event_time and (current_time - self.last_event_time) < self.event_cooldown:
            return False
    
        if next_position.side == PositionSide.LONG:
            should_exit = self._long_exit_conditions(next_position.stop_loss_price, next_position.take_profit_price, ohlcv.low, ohlcv.high, self.risk_buffer)
        elif next_position.side == PositionSide.SHORT:
            should_exit = self._short_exit_conditions(next_position.stop_loss_price, next_position.take_profit_price, ohlcv.low, ohlcv.high, self.risk_buffer)

        if should_exit:
            self.last_event_time = current_time

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
