from core.interfaces.abstract_stream_strategy import AbstractStreamStrategy
from core.interfaces.abstract_ws import AbstractWS


class AsyncRealTimeData:
    def __init__(
        self,
        ws: AbstractWS,
        strategy: AbstractStreamStrategy,
    ):
        self.ws = ws
        self.strategy = strategy

    async def __aenter__(self):
        await self.ws.connect()
        await self.strategy.subscribe()
        return self

    async def __aexit__(self, exc_type, exc_value, traceback):
        await self.strategy.unsubscribe()
        await self.ws.close()
        return self

    def __aiter__(self):
        return self

    async def __anext__(self):
        try:
            data = await self.ws.receive()
            return self.strategy.parse(data)
        except StopAsyncIteration:
            await self.strategy.unsubscribe()
            raise
