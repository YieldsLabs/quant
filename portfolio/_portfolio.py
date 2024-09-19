import asyncio
from contextlib import asynccontextmanager
from typing import Dict, Tuple

from core.models.entity.portfolio import Performance
from core.models.entity.position import Position
from core.models.strategy import Strategy
from core.models.symbol import Symbol
from core.models.timeframe import Timeframe


class PortfolioStorage:
    def __init__(self):
        self._data: Dict[Tuple[Symbol, Timeframe, Strategy], Performance] = {}
        self._lock = asyncio.Lock()

    async def next(self, position: Position, account_size: int, risk_per_trade: float):
        key = self._get_key(
            position.signal.symbol, position.signal.timeframe, position.signal.strategy
        )
        async with self._state() as state:
            performance = state[key] or Performance(account_size, risk_per_trade)
            performance = performance.next(position.pnl, position.fee)
            state[key] = performance
            return performance

    async def get(self, symbol: Symbol, timeframe: Timeframe, strategy: Strategy):
        key = self._get_key(symbol, timeframe, strategy)
        async with self._state() as state:
            return state.get(key)

    async def reset(
        self, symbol, timeframe, strategy, account_size: int, risk_per_trade: float
    ):
        key = self._get_key(symbol, timeframe, strategy)
        async with self._state() as state:
            state[key] = Performance(account_size, risk_per_trade)

    async def reset_all(self):
        async with self._state() as state:
            state.clear()

    async def get_equity(
        self, symbol: Symbol, timeframe: Timeframe, strategy: Strategy
    ):
        performance = await self.get(symbol, timeframe, strategy)
        return performance.equity[-1] if performance and len(performance.equity) else 1

    async def get_kelly(self, symbol: Symbol, timeframe: Timeframe, strategy: Strategy):
        performance = await self.get(symbol, timeframe, strategy)
        return performance.kelly if performance else 0

    async def get_fitness(
        self, symbol: Symbol, timeframe: Timeframe, strategy: Strategy
    ):
        performance = await self.get(symbol, timeframe, strategy)
        return performance.deflated_sharpe_ratio if performance else 0

    @asynccontextmanager
    async def _state(self):
        async with self._lock:
            yield self._data

    @staticmethod
    def _get_key(symbol, timeframe, strategy):
        return (symbol, timeframe, strategy)
