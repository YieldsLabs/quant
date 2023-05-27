from typing import List
from core.events.ohlcv import OHLCV
from .symbol_data import SymbolData


class StrategyStorage:
    def __init__(self, window_size: int):
        self.window_size = window_size
        self.window_data = {}

    def get_symbol_data(self, event_id: str) -> SymbolData:
        return self.window_data.setdefault(event_id, SymbolData(self.window_size))

    async def append(self, event_id: str, event: OHLCV) -> None:
        symbol_data = self.get_symbol_data(event_id)
        await symbol_data.append(event)

    def can_process(self, event_id: str) -> bool:
        return self.get_symbol_data(event_id).count >= self.window_size

    async def get_window(self, event_id: str) -> List[OHLCV]:
        return await self.get_symbol_data(event_id).get_window()
