import asyncio
from contextlib import asynccontextmanager
from typing import List, Optional, Tuple

from core.models.position import Position
from core.models.side import PositionSide
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
            key = self._get_key(position.signal.symbol, position.signal.timeframe)
            long, short = data.get(key, (None, None))

            data[key] = (
                position if position.side == PositionSide.LONG else long,
                position if position.side == PositionSide.SHORT else short,
            )

            return data.get(key, (None, None))

    async def delete_position(self, position: Position):
        async with self._locked_data() as data:
            key = self._get_key(position.signal.symbol, position.signal.timeframe)
            long, short = data.get(key, (None, None))

            data[key] = (
                None if position.side == PositionSide.LONG else long,
                None if position.side == PositionSide.SHORT else short,
            )

    async def position_exists(self, symbol: Symbol, timeframe: Timeframe) -> bool:
        async with self._locked_data() as data:
            key = self._get_key(symbol, timeframe)
            long, short = data.get(key, (None, None))

            return any(position is not None for position in (long, short))

    async def position_long_exists(self, symbol: Symbol, timeframe: Timeframe) -> bool:
        async with self._locked_data() as data:
            key = self._get_key(symbol, timeframe)
            long, _ = data.get(key, (None, None))

            return long

    async def position_short_exists(self, symbol: Symbol, timeframe: Timeframe) -> bool:
        async with self._locked_data() as data:
            key = self._get_key(symbol, timeframe)
            _, short = data.get(key, (None, None))

            return short

    async def retrieve_all_positions(self) -> List[Position]:
        async with self._locked_data() as data:
            return [
                position
                for positions in data.values()
                for position in positions
                if position is not None
            ]

    async def retrieve_position(
        self, symbol: Symbol, timeframe: Timeframe
    ) -> Tuple[Optional[Position], Optional[Position]]:
        async with self._locked_data() as data:
            key = self._get_key(symbol, timeframe)

            return data.get(key, (None, None))

    async def update_stored_position(self, position: Position) -> Position:
        long, short = await self.store_position(position)
        return long if position.side == PositionSide.LONG else short

    async def close_stored_position(self, position: Position):
        await self.delete_position(position)
