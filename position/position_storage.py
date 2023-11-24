import asyncio
from contextlib import asynccontextmanager
from typing import Optional

from core.models.position import Position
from core.models.symbol import Symbol
from core.models.timeframe import Timeframe


class PositionStorage:
    def __init__(self):
        self.data = {}
        self._lock = asyncio.Lock()

    @asynccontextmanager
    async def _locked_data(self):
        async with self._lock:
            yield self.data

    def _get_key(self, symbol: Symbol, timeframe: Timeframe) -> tuple:
        return (symbol, timeframe)

    async def store_position(self, position: Position):
        async with self._locked_data() as data:
            data[
                self._get_key(position.signal.symbol, position.signal.timeframe)
            ] = position

    async def delete_position(self, position: Position):
        async with self._locked_data() as data:
            data.pop(
                self._get_key(position.signal.symbol, position.signal.timeframe), None
            )

    async def position_exists(self, symbol: Symbol, timeframe: Timeframe) -> bool:
        async with self._locked_data() as data:
            return self._get_key(symbol, timeframe) in data

    async def retrieve_all_positions(self) -> list:
        async with self._locked_data() as data:
            return list(data.values())

    async def retrieve_position(
        self, symbol: Symbol, timeframe: Timeframe
    ) -> Optional[Position]:
        async with self._locked_data() as data:
            return data.get(self._get_key(symbol, timeframe))

    async def update_stored_position(self, position: Position):
        symbol = position.signal.symbol
        timeframe = position.signal.timeframe

        existing_position = await self._extract_position(symbol, timeframe)

        if existing_position:
            await self.store_position(position)

    async def close_stored_position(self, position: Position):
        symbol = position.signal.symbol
        timeframe = position.signal.timeframe

        await self._extract_position(symbol, timeframe)

    async def _extract_position(
        self, symbol: Symbol, timeframe: Timeframe
    ) -> Optional[Position]:
        position = await self.retrieve_position(symbol, timeframe)

        if position:
            await self.delete_position(position)

        return position
