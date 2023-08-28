import asyncio
from typing import Optional
from contextlib import asynccontextmanager

from core.models.position import Position
from core.models.signal import Signal


class PositionStorage:
    def __init__(self):
        super().__init__()
        self.data = {}
        self._lock = asyncio.Lock()

    @asynccontextmanager
    async def _locked_data(self):
        async with self._lock:
            yield self.data

    async def open_position(self, position: Position):
       async with self._locked_data() as data:
            key = (position.signal.symbol, position.signal.timeframe)
            data[key] = position

    async def remove_position(self, position: Position):
        async with self._locked_data() as data:
            key = (position.signal.symbol, position.signal.timeframe)
            data.pop(key, None)
    
    async def has_position(self, signal: Signal):
        async with self._locked_data() as data:
            key = (signal.symbol, signal.timeframe)
            
            return key in data

    async def get_positions(self):
        async with self._locked_data() as data:
            return list(data.values())

    async def get_position(self, signal: Signal):
        async with self._locked_data() as data:
            key = (signal.symbol, signal.timeframe)
            
            return data.get(key)

    async def update_position(self, position: Position):
        stored_position = await self._fetch_and_remove_position(position)
        
        if stored_position:
            await self.open_position(position)

    async def close_position(self, position: Position):
        await self._fetch_and_remove_position(position)

    async def _fetch_and_remove_position(self, position: Position) -> Optional[Position]:
        stored_position = await self.get_position(position.signal)
        
        if stored_position:
            await self.remove_position(stored_position)
        
        return stored_position
