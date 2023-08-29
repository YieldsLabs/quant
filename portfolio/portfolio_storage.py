import asyncio
from typing import Dict

from core.models.portfolio import Performance
from core.models.position import Position
from core.models.signal import Signal
from core.models.strategy import Strategy


class PortfolioStorage:
    def __init__(self):
        self.data: Dict[Strategy, Performance] = {}
        self._lock = asyncio.Lock()

    async def next(self, position: Position, account_size: int, risk_per_trade: float):
        async with self._lock:
            key = position.signal
            performance = self.data.get(key)

            if performance:
                self.data[key] = performance.next(position.pnl)
            else:
                self.data[key] = Performance(account_size, risk_per_trade).next(position.pnl)

    async def get(self, position: Position):
        async with self._lock:
            return self.data.get(position.signal)

    async def get_total_pnl(self, signal: Signal):
        async with self._lock:
            performance = self.data.get(signal)
            return performance.total_pnl if performance else 0
   
    async def get_top_signals(self, num: int):
        async with self._lock:
            sorted_signals = sorted(self.data.keys(), key=lambda signal: self.data[signal].total_pnl, reverse=True)
            return sorted_signals[:num]

    

    