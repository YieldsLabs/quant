import asyncio
import logging
from typing import List

from core.actors import StrategyActor
from core.commands.feed import StartRealtimeFeed
from core.events.ohlcv import NewMarketDataReceived
from core.interfaces.abstract_timeseries import AbstractTimeSeriesService
from core.interfaces.abstract_ws import AbstractWS
from core.models.entity.bar import Bar
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


class RealtimeActor(StrategyActor):
    def __init__(
        self,
        symbol: Symbol,
        timeframe: Timeframe,
        ws: AbstractWS,
        ts: AbstractTimeSeriesService,
    ):
        super().__init__(symbol, timeframe)
        self.queue = asyncio.Queue()
        self.ws = ws
        self.ts = ts
        self.producer = None
        self.consumer = None

    def on_stop(self):
        if self.producer:
            self.producer.cancel()

        if self.consumer:
            self.consumer.cancel()

    async def on_receive(self, _msg: StartRealtimeFeed):
        self.producer = asyncio.create_task(self._producer())
        self.consumer = asyncio.create_task(self._consumer())

    async def _producer(self):
        async with AsyncRealTimeData(self.ws, self.symbol, self.timeframe) as stream:
            async for bars in stream:
                await self.queue.put(bars)

            await self.queue.put(None)

    async def _consumer(self):
        while True:
            bars = await self.queue.get()

            if bars is None:
                break

            await self._process_bars(bars)

            self.queue.task_done()

    async def _process_bars(self, bars: List[Bar]):
        for bar in bars:
            if bar.closed:
                await self.ts.upsert(self.symbol, self.timeframe, bar.ohlcv)

                logger.info(f"{self.symbol}_{self.timeframe}:{bar}")

            await self.tell(
                NewMarketDataReceived(
                    self.symbol, self.timeframe, bar
                )
            )
