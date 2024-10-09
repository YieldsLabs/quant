from core.interfaces.abstract_exchange import AbstractWSExchange
from core.interfaces.abstract_stream_strategy import AbstractStreamStrategy


class AsyncRealTimeData:
    def __init__(
        self,
        ws: AbstractWSExchange,
        strategy: AbstractStreamStrategy,
    ):
        self.ws = ws
        self.strategy = strategy

    async def __aenter__(self) -> "AsyncRealTimeData":
        await self.ws.connect()
        await self.strategy.subscribe(self.ws)
        return self

    async def __aexit__(self, exc_type, exc_value, traceback):
        await self.strategy.unsubscribe(self.ws)
        await self.ws.close()
        return self

    def __aiter__(self) -> "AsyncRealTimeData":
        return self

    async def __anext__(self):
        try:
            return await self.strategy.next(self.ws)
        except StopAsyncIteration:
            await self.strategy.unsubscribe()
            raise
