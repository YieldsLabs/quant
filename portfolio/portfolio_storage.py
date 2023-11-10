import asyncio
from typing import Dict

from core.models.portfolio import Performance
from core.models.position import Position
from core.models.strategy import Strategy
from core.models.symbol import Symbol
from core.models.timeframe import Timeframe


class PortfolioStorage:
    def __init__(self):
        self.data: Dict[Strategy, Performance] = {}
        self._lock = asyncio.Lock()

    async def next(self, position: Position, account_size: int, risk_per_trade: float):
        async with self._lock:
            key = self._get_key(
                position.signal.symbol,
                position.signal.timeframe,
                position.signal.strategy,
            )
            performance = self.data.get(key)

            if performance:
                self.data[key] = performance.next(position.pnl)
            else:
                self.data[key] = Performance(account_size, risk_per_trade).next(
                    position.pnl
                )

    async def get(self, position: Position):
        async with self._lock:
            key = self._get_key(
                position.signal.symbol,
                position.signal.timeframe,
                position.signal.strategy,
            )

            return self.data.get(key)

    async def reset(self, symbol, timeframe, strategy):
        async with self._lock:
            key = self._get_key(symbol, timeframe, strategy)
            self.data[key] = {}

    async def get_total_pnl(
        self, symbol: Symbol, timeframe: Timeframe, strategy: Strategy
    ):
        async with self._lock:
            key = self._get_key(symbol, timeframe, strategy)
            performance = self.data.get(key)

            return performance.total_pnl if performance else 0

    async def get_pnl(self):
        async with self._lock:
            return sum(
                [
                    performance.total_pnl
                    for performance in self.data.values()
                    if performance
                ]
            )

    async def annualized_return(self):
        async with self._lock:
            return sum(
                [
                    performance.annualized_return
                    for performance in self.data.values()
                    if performance
                ]
            )

    async def get_fitness(
        self, symbol: Symbol, timeframe: Timeframe, strategy: Strategy
    ):
        async with self._lock:
            key = self._get_key(symbol, timeframe, strategy)
            performance = self.data.get(key)

            return performance.sharpe_ratio if performance else 0

    def _get_key(self, symbol, timeframe, strategy):
        return f"{symbol}_{timeframe}{strategy}"
