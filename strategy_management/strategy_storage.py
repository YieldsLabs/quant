from collections import defaultdict
import asyncio
from typing import List
from core.events.ohlcv import OHLCV
from core.timeframe import Timeframe

from strategy_management.symbol_data import SymbolData


class StrategyStorage:
    def __init__(self, window_size: int):
        self.window_size = window_size
        self.window_data = defaultdict(lambda: SymbolData(self.window_size))
        self.lock = asyncio.Lock()

    async def append(self, symbol: str, timeframe: Timeframe, event: OHLCV) -> None:
        async with self.lock:
            symbol_data = self.window_data[(symbol, timeframe)]
            await symbol_data.append(event)

    async def can_process(self, symbol: str, timeframe: Timeframe) -> bool:
        async with self.lock:
            symbol_data = self.window_data[(symbol, timeframe)]
            return symbol_data.count >= self.window_size

    async def get_window(self, symbol: str, timeframe: Timeframe) -> List[OHLCV]:
        async with self.lock:
            symbol_data = self.window_data[(symbol, timeframe)]
            return await symbol_data.get_window()
