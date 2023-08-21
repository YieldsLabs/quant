import asyncio

from core.models.position import PositionSide
from core.models.timeframe import Timeframe


class BreakEvenStopLossStrategy:
    def __init__(self):
        self.data = {}
        self.lock = asyncio.Lock()

    async def _init(self, loss_id: str):
        async with self.lock:
            self.data[loss_id] = {PositionSide.LONG: None, PositionSide.SHORT: None}

    async def next(self, strategy: str, position_side: PositionSide, position_size: float, stop_loss_price: float, entry_price: float, low: float, high: float, risk_per_trade: float) -> float:
        if strategy not in self.data:
            await self._init(strategy)

        if not self.data[strategy][position_side]:
            self.data[strategy][position_side] = stop_loss_price

        self.data[strategy][position_side] = self._calculate_stop_loss(strategy, position_side, position_size, stop_loss_price, entry_price, low, high, risk_per_trade)

        return self.data[strategy][position_side]

    def _calculate_stop_loss(self, strategy, position_side, position_size, stop_loss_price, entry_price, low, high, risk_per_trade):
        new_stop_loss_price = high - (high - stop_loss_price) * risk_per_trade if position_side == PositionSide.LONG else low + (stop_loss_price - low) * risk_per_trade

        if ((position_side == PositionSide.LONG and new_stop_loss_price > self.data[strategy][position_side])
                or (position_side == PositionSide.SHORT and new_stop_loss_price < self.data[strategy][position_side])):
            self.data[strategy][position_side] = new_stop_loss_price

        if abs(self.data[strategy][position_side] - entry_price) >= risk_per_trade * position_size:
            self.data[strategy][position_side] = entry_price

        return self.data[strategy][position_side]

    async def reset(self, strategy: str, position_side: PositionSide):
        async with self.lock:
            if strategy in self.data:
                self.data[strategy][position_side] = None
