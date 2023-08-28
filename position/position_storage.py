import asyncio
from collections import namedtuple
from typing import Optional

from core.commands.position import PositionClose, PositionCloseAll, PositionOpen, PositionUpdate
from core.event_decorators import command_handler, query_handler
from core.interfaces.abstract_position_storage import AbstractPositionStorage
from core.models.position import Position
from core.models.signal import Signal
from core.queries.position import PositionAll, PositionActive, PositionBySignal


from contextlib import asynccontextmanager

class PositionStorage(AbstractPositionStorage):
    def __init__(self):
        super().__init__()
        self.data = {}
        self._positions_lock = asyncio.Lock()

    @asynccontextmanager
    async def _locked_data(self):
        async with self._positions_lock:
            yield self.data

    async def _open_position(self, signal: Signal, position: Position):
        async with self._locked_data() as data:
            data[signal.symbol] = position

    async def _remove_position(self, signal: Signal):
        async with self._locked_data() as data:
            data.pop(signal.symbol, None)

    async def _get_position(self, signal: Signal) -> Optional[Position]:
        async with self._locked_data() as data:
            return data.get(signal.symbol)

    async def _get_all(self) -> list[Position]:
        async with self._locked_data() as data:
            return list(data.values())

    async def _fetch_and_remove_position(self, signal: Signal) -> Optional[Position]:
        position = await self._get_position(signal)
        if position:
            await self._remove_position(signal)
        return position

    @command_handler(PositionOpen)
    async def open_position(self, command: PositionOpen):
        await self._open_position(command.position.signal, command.position)

    @query_handler(PositionActive)
    async def has_position(self, query: PositionActive):
        async with self._locked_data() as data:
            return query.signal.symbol in data

    @query_handler(PositionAll)
    async def get_positions(self, _query: PositionAll):
        return await self._get_all()

    @query_handler(PositionBySignal)
    async def get_position(self, query: PositionBySignal):
        return await self._get_position(query.signal)

    @command_handler(PositionUpdate)
    async def update_position(self, command: PositionUpdate):
        signal = command.position.signal
        position = await self._fetch_and_remove_position(signal)
        if position:
            await self._open_position(signal, command.position)

    @command_handler(PositionClose)
    async def close_position(self, command: PositionClose):
        await self._fetch_and_remove_position(command.position.signal)

    @command_handler(PositionCloseAll)
    async def close_all(self, _command: PositionCloseAll):
        positions = await self._get_all()
        for position in positions:
            await self._fetch_and_remove_position(position.signal)
