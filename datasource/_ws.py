import asyncio

from core.interfaces.abstract_datasource import AbstractDataSource
from core.interfaces.abstract_ws import AbstractWS
from core.models.symbol import Symbol
from core.models.timeframe import Timeframe


class AsyncRealTimeData:
    def __init__(
        self,
        ws: AbstractWS,
        symbol: Symbol,
        timeframe: Timeframe,
    ):
        self.ws = ws
        self.symbol = symbol
        self.timeframe = timeframe
        self.iterator = None

    async def _init_iterator(self) -> None:
        if self.iterator is None:
            asyncio.create_task(self.ws.run())
            await self.ws.subscribe(self.symbol, self.timeframe)

            self.iterator = self.ws

    async def __aenter__(self):
        await self._init_iterator()

    async def __aexit__(self, exc_type, exc_value, traceback):
        await self.ws.close()

    def __aiter__(self):
        return self

    async def __anext__(self):
        await self._init_iterator()

        try:
            bar = await self.iterator.receive()
            return bar
        except StopAsyncIteration:
            await self.ws.close()
            raise


class WSDataSource(AbstractDataSource):
    def __init__(self, ws: AbstractWS, symbol: Symbol, timeframe: Timeframe):
        super().__init__()
        self.ws = ws
        self.symbol = symbol
        self.timeframe = timeframe

    def fetch(self):
        return AsyncRealTimeData(self.ws, self.symbol, self.timeframe)
