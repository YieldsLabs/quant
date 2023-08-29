import asyncio
from typing import Dict, Tuple

from core.models.position import Position
from core.models.strategy import Strategy
from portfolio.performance import Performance


class PortfolioStorage:
    def __init__(self):
        self.data: Dict[Strategy, Tuple[Performance]] = {}
        self._lock = asyncio.Lock()

    async def update(self, position: Position, account_size: int, risk_per_trade: float):
        async with self._lock:
            (performance) = self.data.get(position.signal.strategy, (Performance(account_size, risk_per_trade)))
            performance.next(position.pnl)
            self.data[position.signal.strategy] = (performance)

    async def get_total_pnl(self, position: Position):
        async with self._lock:
            data = self.data.get(position.signal.strategy)
            return data[0].total_pnl if data else 0

        
    async def get_top_strategy(self, position: Position):
        async with self._lock:
            return ''

    

    