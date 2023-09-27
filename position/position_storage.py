import asyncio
from contextlib import asynccontextmanager
from typing import Optional

from core.models.position import Position
from core.models.signal import Signal


class PositionStorage:
    def __init__(self):
        self.data = {}
        self._lock = asyncio.Lock()

    @asynccontextmanager
    async def _locked_data(self):
        async with self._lock:
            yield self.data

    def _get_key(self, signal: Signal) -> tuple:
        return (signal.symbol, signal.timeframe)

    async def store_position(self, position: Position):
        async with self._locked_data() as data:
            data[self._get_key(position.signal)] = position

    async def delete_position(self, position: Position):
        async with self._locked_data() as data:
            data.pop(self._get_key(position.signal), None)

    async def position_exists(self, signal: Signal) -> bool:
        async with self._locked_data() as data:
            return self._get_key(signal) in data

    async def retrieve_all_positions(self) -> list:
        async with self._locked_data() as data:
            return list(data.values())

    async def retrieve_position(self, signal: Signal) -> Optional[Position]:
        async with self._locked_data() as data:
            return data.get(self._get_key(signal))

    async def update_stored_position(self, position: Position):
        existing_position = await self._extract_position(position.signal)

        if existing_position:
            await self.store_position(position)

    async def close_stored_position(self, position: Position):
        await self._extract_position(position.signal)

    async def _extract_position(self, signal: Signal) -> Optional[Position]:
        position = await self.retrieve_position(signal)

        if position:
            await self.delete_position(position)

        return position
