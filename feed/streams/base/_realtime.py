from core.interfaces.abstract_stream_strategy import AbstractStreamStrategy


class AsyncRealTimeData:
    def __init__(
        self,
        strategy: AbstractStreamStrategy,
    ):
        self.strategy = strategy

    async def __aenter__(self):
        await self.strategy.subscribe()
        return self

    async def __aexit__(self, exc_type, exc_value, traceback):
        await self.strategy.unsubscribe()
        return self

    def __aiter__(self):
        return self

    async def __anext__(self):
        try:
            data = await self.strategy.receive()
            return data
        except StopAsyncIteration:
            await self.strategy.unsubscribe()
            raise
