import asyncio
import logging
from typing import List

from core.actors import StrategyActor
from core.commands.ohlcv import IngestMarketData
from core.events.ohlcv import NewMarketDataReceived
from core.interfaces.abstract_ws import AbstractWS
from core.models.entity.bar import Bar
from core.models.symbol import Symbol
from core.models.timeframe import Timeframe
from core.tasks.feed import StartRealtimeFeed

from .streams.base import AsyncRealTimeData
from .streams.strategy.kline import KlineStreamStrategy

logger = logging.getLogger(__name__)


class RealtimeActor(StrategyActor):
    def __init__(
        self,
        symbol: Symbol,
        timeframe: Timeframe,
        ws: AbstractWS,
    ):
        super().__init__(symbol, timeframe)
        self.queue = asyncio.Queue()
        self.ws = ws
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
        async with AsyncRealTimeData(
            self.ws,
            KlineStreamStrategy(self.ws, self.timeframe, self.symbol)
        ) as stream:
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
            await self.ask(IngestMarketData(self.symbol, self.timeframe, bar))
            await self.tell(NewMarketDataReceived(self.symbol, self.timeframe, bar))

            if bar.closed:
                logger.info(f"{self.symbol}_{self.timeframe}:{bar}")
