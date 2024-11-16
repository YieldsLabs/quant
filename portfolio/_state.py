import asyncio
from contextlib import asynccontextmanager
from typing import Dict, Tuple

from core.models.entity.portfolio import Performance
from core.models.entity.position import Position
from core.models.strategy import Strategy
from core.models.symbol import Symbol
from core.models.timeframe import Timeframe


class PortfolioState:
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

    async def init(
        self, symbol, timeframe, strategy, account_size: int, risk_per_trade: float
    ):
        key = self._get_key(symbol, timeframe, strategy)
        async with self._state() as state:
            state[key] = Performance(account_size, risk_per_trade)

    async def reset_all(self):
        async with self._state() as state:
            state.clear()

    @asynccontextmanager
    async def _state(self):
        async with self._lock:
            yield self._data

    @staticmethod
    def _get_key(symbol, timeframe, strategy):
        return symbol, timeframe, strategy
