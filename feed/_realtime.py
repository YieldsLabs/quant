import asyncio
import logging

from core.actors import StrategyActor
from core.commands.feed import StartRealtimeFeed
from core.events.ohlcv import NewMarketDataReceived
from core.interfaces.abstract_ws import AbstractWS
from core.models.symbol import Symbol
from core.models.timeframe import Timeframe

logger = logging.getLogger(__name__)


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


class RealtimeActor(StrategyActor):
    _EVENTS = [StartRealtimeFeed]

    def __init__(
        self,
        symbol: Symbol,
        timeframe: Timeframe,
        ws: AbstractWS,
    ):
        super().__init__(symbol, timeframe)
        self.ws = ws
        self.task = None

    def on_stop(self):
        if self.task:
            self.task.cancel()

        asyncio.create_task(self.ws.unsubscribe(self.symbol, self.timeframe))

    async def on_receive(self, msg: StartRealtimeFeed):
        self.task = asyncio.create_task(self._run_realtime_feed(msg))

    async def _run_realtime_feed(self, msg: StartRealtimeFeed):
        symbol, timeframe = msg.symbol, msg.timeframe

        async with AsyncRealTimeData(self.ws, symbol, timeframe) as stream:
            async for bar in stream:
                if bar:
                    await self.tell(
                        NewMarketDataReceived(symbol, timeframe, bar.ohlcv, bar.closed)
                    )

                if bar and bar.closed:
                    logger.info(f"{symbol}_{timeframe}:{bar}")
