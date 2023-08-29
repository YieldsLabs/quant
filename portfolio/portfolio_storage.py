import asyncio
from typing import Dict, List

from core.models.position import Position
from core.models.strategy import Strategy


class PortfolioStorage:
    def __init__(self):
        self.data: Dict[Strategy, List[Position]] = {}
        self._lock = asyncio.Lock()

    async def update(self, position: Position):
        async with self._lock:
            pnl = self.data.get(position.signal.strategy, [])
            pnl.append(position.pnl)
            self.data[position.signal.strategy] = pnl

    async def get_pnl(self, position: Position):
        async with self._lock:
            return 0
        
    async def get_top_strategy(self, position: Position):
        async with self._lock:
            return ''

    

    