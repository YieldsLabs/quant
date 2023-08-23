from typing import Type

from core.events.ohlcv import NewMarketDataReceived
from core.interfaces.abstract_actor import AbstractActor
from core.interfaces.abstract_position_storage import AbstractPositionStorage
from core.interfaces.abstract_risk_strategy import AbstractRiskStrategy
from core.models.ohlcv import OHLCV
from core.events.risk import RiskThresholdBreached
from core.models.position import PositionSide

from .position_risk_take_profit import PositionTakeProfit


class PositionRiskActor(AbstractActor):
    def __init__(self, 
                risk_strategy: Type[AbstractRiskStrategy],
                position_storage: Type[AbstractPositionStorage],
        ):
        super().__init__()
        self.risk_strategy = risk_strategy
        self.position_storage = position_storage
        self._strategy = None
        self._running = False

    @property
    def strategy(self) -> str:
        return self._strategy
    
    @property
    def running(self):
        return self._running 
    
    def start(self):
        if self.running:
            raise RuntimeError("Start: risk is running")

        self._running = True
        self.dispatcher.register(NewMarketDataReceived, self._risk_event_filter)

    def stop(self):
        if not self.running:
            raise RuntimeError("Stop: risk is not started")
        
        self._running = False
        self.dispatcher.unregister(NewMarketDataReceived, self._risk_event_filter)
    
    async def next(self, event: NewMarketDataReceived):
        position = await self.position_storage.get_active_position(event.symbol)

        if position is None:
            return
        
        self._strategy = position.strategy

        take_profit_price = PositionTakeProfit.calculate(position.entry_price, position.stop_loss_price, position.risk_reward_ratio)

        stop_loss_price = await self.risk_strategy.next(self.strategy, position.side, position.size, position.stop_loss_price, position.entry_price, position.risk_per_trade, event.ohlcv)

        if self._should_exit(position.side, stop_loss_price, take_profit_price, event.ohlcv):
            await self._process_exit(self.strategy, position.side, event.ohlcv, take_profit_price, stop_loss_price)

    async def _risk_event_filter(self, event: NewMarketDataReceived):
        if await self.position_storage.has_active_position(event.symbol):
            await self.next(event)

    async def _process_exit(self, strategy, position_side, ohlcv, take_profit_price, stop_loss_price):
        await self.risk_strategy.reset(strategy, position_side)

        exit_price = self._calculate_exit_price(position_side, ohlcv.close, take_profit_price, stop_loss_price)

        await self.dispatcher.dispatch(RiskThresholdBreached(strategy=strategy, side=position_side, exit=exit_price))

    def _should_exit(self, position_side: PositionSide, stop_loss_price: float | None, take_profit_price: float | None, ohlcv: OHLCV):
        if position_side == PositionSide.LONG:
            return self._long_exit_conditions(stop_loss_price, take_profit_price, ohlcv.low, ohlcv.high)
        elif position_side == PositionSide.SHORT:
            return self._short_exit_conditions(stop_loss_price, take_profit_price, ohlcv.low, ohlcv.high)

    @staticmethod
    def _calculate_exit_price(position_side: PositionSide, current_close: float, take_profit_price: float | None, stop_loss_price: float | None):
        exit_price = current_close

        if position_side == PositionSide.LONG:
            exit_price = max(min(current_close, take_profit_price or current_close),
                             stop_loss_price or current_close)
        elif position_side == PositionSide.SHORT:
            exit_price = min(max(current_close, take_profit_price or current_close),
                             stop_loss_price or current_close)
        return exit_price

    @staticmethod
    def _long_exit_conditions(stop_loss_price: float | None, take_profit_price: float | None, low: float, high: float):
        return (stop_loss_price is not None and low <= stop_loss_price) or \
               (take_profit_price is not None and high >= take_profit_price)

    @staticmethod
    def _short_exit_conditions(stop_loss_price: float | None, take_profit_price: float | None, low: float, high: float):
        return (stop_loss_price is not None and high >= stop_loss_price) or \
               (take_profit_price is not None and low <= take_profit_price)
