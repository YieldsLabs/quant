import asyncio
import logging
from typing import List

from core.actors import StrategyActor
from core.commands.ohlcv import IngestMarketData
from core.events.ohlcv import NewMarketDataReceived
from core.interfaces.abstract_exhange_factory import AbstractExchangeFactory
from core.models.entity.bar import Bar
from core.models.symbol import Symbol
from core.models.timeframe import Timeframe
from core.tasks.feed import StartRealtimeFeed

from .streams.base import AsyncRealTimeData
from .streams.collector import DataCollector
from .streams.strategy import (
    KlineStreamStrategy,
    OrderBookStreamStrategy,
)

logger = logging.getLogger(__name__)


class RealtimeActor(StrategyActor):
    def __init__(
        self,
        symbol: Symbol,
        timeframe: Timeframe,
        ws_factory: AbstractExchangeFactory,
    ):
        super().__init__(symbol, timeframe)
        self.ws_factory = ws_factory
        self.collector = DataCollector()

        self.collector.add_producer(self._kline_producer)
        self.collector.add_producer(self._ob_producer)
        self.collector.add_consumer(self._consumer)

        self.depth = 50

    def on_stop(self):
        asyncio.create_task(self.collector.stop())

    async def on_receive(self, msg: StartRealtimeFeed):
        await self.collector.start(msg)

    async def _kline_producer(self, msg: StartRealtimeFeed):
        ws = self.ws_factory.create(msg.exchange)

        async with AsyncRealTimeData(
            ws, KlineStreamStrategy(ws, self.timeframe, self.symbol)
        ) as stream:
            async for bars in stream:
                yield bars

    async def _ob_producer(self, msg: StartRealtimeFeed):
        ws = self.ws_factory.create(msg.exchange)
        async with AsyncRealTimeData(
            ws, OrderBookStreamStrategy(ws, self.symbol, self.depth)
        ) as stream:
            async for orders in stream:
                yield orders

    async def _consumer(self, data: List[Bar]):
        match data:
            case [Bar(), *_]:
                await self._process_bars(data)

    async def _process_bars(self, bars: List[Bar]):
        for bar in bars:
            print(bar)
            await self.ask(IngestMarketData(self.symbol, self.timeframe, bar))
            await self.tell(NewMarketDataReceived(self.symbol, self.timeframe, bar))

            if bar.closed:
                logger.info(f"{self.symbol}_{self.timeframe}:{bar}")
