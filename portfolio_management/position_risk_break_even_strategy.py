import asyncio
from collections import namedtuple

from core.interfaces.abstract_risk_strategy import AbstractRiskStrategy
from core.models.ohlcv import OHLCV
from core.models.position import PositionSide
from core.models.strategy import Strategy


StrategyState = namedtuple("StrategyState", ["long", "short"])

class BreakEvenStrategy(AbstractRiskStrategy):
    def __init__(self):
        self.state = {}
        self.lock = asyncio.Lock()

    async def next(self, strategy: Strategy, position_side: PositionSide, position_size: float, stop_loss_price: float, entry_price: float, risk_per_trade: float, ohlcv: OHLCV) -> float:
        async with self.lock:
            if stop_loss_price is None:
                return
            
            current_state = self.state.get(strategy, StrategyState(None, None))
            
            if current_state.long is None and position_side == PositionSide.LONG:
                current_state = current_state._replace(long=stop_loss_price)
            elif current_state.short is None and position_side == PositionSide.SHORT:
                current_state = current_state._replace(short=stop_loss_price)

            new_stop_loss = self._calculate_stop_loss(strategy, position_side, position_size, stop_loss_price, entry_price, ohlcv.low, ohlcv.high, risk_per_trade)
            
            if position_side == PositionSide.LONG:
                current_state = current_state._replace(long=new_stop_loss)
            else:
                current_state = current_state._replace(short=new_stop_loss)

            self.state[strategy] = current_state

            return new_stop_loss if position_side == PositionSide.LONG else current_state.short

    async def reset(self, strategy: Strategy, position_side: PositionSide):
        async with self.lock:
            if strategy in self.state:
                current_state = self.state[strategy]
                
                if position_side == PositionSide.LONG:
                    current_state = current_state._replace(long=None)
                else:
                    current_state = current_state._replace(short=None)
                
                self.state[strategy] = current_state

    def _calculate_stop_loss(self, strategy, position_side, position_size, stop_loss_price, entry_price, low, high, risk_per_trade):
        current_state = self.state.get(strategy, StrategyState(None, None))
        new_stop_loss_price = high - (high - stop_loss_price) * risk_per_trade if position_side == PositionSide.LONG else low + (stop_loss_price - low) * risk_per_trade

        current_value = current_state.long if position_side == PositionSide.LONG else current_state.short

        if current_value is None:
            return new_stop_loss_price

        if (position_side == PositionSide.LONG and new_stop_loss_price > current_value) or (position_side == PositionSide.SHORT and new_stop_loss_price < current_value):
            return new_stop_loss_price

        if abs(current_value - entry_price) >= risk_per_trade * position_size:
            return entry_price

        return current_value
