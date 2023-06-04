import asyncio

from core.position import PositionSide
from core.timeframe import Timeframe


class BreakEvenStopLossStrategy:
    def __init__(self):
        self.data = {}
        self.lock = asyncio.Lock()

    async def _init(self, loss_id: str):
        async with self.lock:
            self.data[loss_id] = {PositionSide.LONG: None, PositionSide.SHORT: None}

    async def next(self, symbol: str, timeframe: Timeframe, position_side: PositionSide, position_size: float, stop_loss_price: float, entry_price: float, low: float, high: float, risk_per_trade: float) -> float:
        loss_id = self._create_loss_id(symbol, timeframe)

        if loss_id not in self.data:
            await self._init(loss_id)

        if not self.data[loss_id][position_side]:
            self.data[loss_id][position_side] = stop_loss_price

        self.data[loss_id][position_side] = self._calculate_stop_loss(loss_id, position_side, position_size, stop_loss_price, entry_price, low, high, risk_per_trade)

        return self.data[loss_id][position_side]

    def _calculate_stop_loss(self, loss_id, position_side, position_size, stop_loss_price, entry_price, low, high, risk_per_trade):
        new_stop_loss_price = high - (high - stop_loss_price) * risk_per_trade if position_side == PositionSide.LONG else low + (stop_loss_price - low) * risk_per_trade

        if ((position_side == PositionSide.LONG and new_stop_loss_price > self.data[loss_id][position_side])
                or (position_side == PositionSide.SHORT and new_stop_loss_price < self.data[loss_id][position_side])):
            self.data[loss_id][position_side] = new_stop_loss_price

        if abs(self.data[loss_id][position_side] - entry_price) >= risk_per_trade * position_size:
            self.data[loss_id][position_side] = entry_price

        return self.data[loss_id][position_side]

    async def reset(self, symbol: str, timeframe: Timeframe, position_side: PositionSide):
        async with self.lock:
            loss_id = self._create_loss_id(symbol, timeframe)
            self.data[loss_id][position_side] = None

    @staticmethod
    def _create_loss_id(symbol: str, timeframe: Timeframe) -> str:
        return f'{symbol}_{timeframe}'
