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

    async def __aenter__(self):
        await self.ws.subscribe(self.symbol, self.timeframe)
        await self.ws.run()
        return self

    async def __aexit__(self, exc_type, exc_value, traceback):
        await self.ws.unsubscribe(self.symbol, self.timeframe)
        await self.ws.close()
        return self

    def __aiter__(self):
        return self

    async def __anext__(self):
        try:
            data = await self.ws.receive(self.symbol, self.timeframe)
            return data
        except StopAsyncIteration:
            await self.ws.unsubscribe(self.symbol, self.timeframe)
            raise
