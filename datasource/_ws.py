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

        self.task = asyncio.create_task(self._initialize())

    async def _initialize(self):
        await self.ws.run()
        await self.ws.subscribe(self.symbol, self.timeframe)

    async def __aexit__(self, exc_type, exc_value, traceback):
        self.task.cancel()
        await self.ws.close()

    def __aiter__(self):
        return self

    async def __anext__(self):
        try:
            data = await self.ws.receive()
            return data
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
