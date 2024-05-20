import asyncio
from typing import Dict, Tuple

from core.models.portfolio import Performance
from core.models.position import Position
from core.models.strategy import Strategy
from core.models.symbol import Symbol
from core.models.timeframe import Timeframe


class PortfolioStorage:
    def __init__(self):
        self.data: Dict[Tuple[Symbol, Timeframe, Strategy], Performance] = {}
        self._lock = asyncio.Lock()

    async def next(self, position: Position, account_size: int, risk_per_trade: float):
        async with self._lock:
            key = self._get_key(
                position.signal.symbol,
                position.signal.timeframe,
                position.signal.strategy,
            )

            performance = self.data.get(key, None)

            if not performance:
                performance = Performance(account_size, risk_per_trade)

            if abs(position.pnl) != 0:
                performance = performance.next(position.pnl, position.fee)

            self.data[key] = performance

            return performance

    async def get(self, symbol: Symbol, timeframe: Timeframe, strategy: Strategy):
        async with self._lock:
            key = self._get_key(symbol, timeframe, strategy)
            return self.data.get(key, None)

    async def reset(
        self, symbol, timeframe, strategy, account_size: int, risk_per_trade: float
    ):
        async with self._lock:
            key = self._get_key(symbol, timeframe, strategy)
            self.data[key] = Performance(account_size, risk_per_trade)

    async def reset_all(self):
        async with self._lock:
            self.data = {}

    async def get_equity(
        self, symbol: Symbol, timeframe: Timeframe, strategy: Strategy
    ):
        async with self._lock:
            key = self._get_key(symbol, timeframe, strategy)
            performance = self.data.get(key)

            if performance and len(performance.equity) > 2:
                return performance.equity[-1]

            return 1

    async def get_kelly(self, symbol: Symbol, timeframe: Timeframe, strategy: Strategy):
        async with self._lock:
            key = self._get_key(symbol, timeframe, strategy)
            performance = self.data.get(key)

            return performance.kelly if performance else 0

    async def get_optimalf(
        self, symbol: Symbol, timeframe: Timeframe, strategy: Strategy
    ):
        async with self._lock:
            key = self._get_key(symbol, timeframe, strategy)
            performance = self.data.get(key)

            return performance.optimal_f if performance else 0

    async def get_fitness(
        self, symbol: Symbol, timeframe: Timeframe, strategy: Strategy
    ):
        async with self._lock:
            key = self._get_key(symbol, timeframe, strategy)
            performance = self.data.get(key)

            if not performance:
                return 0

            return performance.deflated_sharpe_ratio

    def _get_key(self, symbol, timeframe, strategy):
        return (symbol, timeframe, strategy)
