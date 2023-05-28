from typing import List
from core.events.ohlcv import OHLCV
from core.timeframe import Timeframe
from .symbol_data import SymbolData


class StrategyStorage:
    def __init__(self, window_size: int):
        self.window_size = window_size
        self.window_data = {}

    def get_symbol_data(self, symbol: str, timeframe: Timeframe) -> SymbolData:
        return self.window_data.setdefault(f'{symbol}_{timeframe}', SymbolData(self.window_size))

    async def append(self, symbol: str, timeframe: Timeframe, event: OHLCV) -> None:
        await self.get_symbol_data(symbol, timeframe).append(event)

    def can_process(self, symbol: str, timeframe: Timeframe) -> bool:
        return self.get_symbol_data(symbol, timeframe).count >= self.window_size

    async def get_window(self, symbol: str, timeframe: Timeframe) -> List[OHLCV]:
        return await self.get_symbol_data(symbol, timeframe).get_window()
