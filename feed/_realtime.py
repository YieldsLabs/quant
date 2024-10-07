import asyncio
import logging
from typing import List

from coral import DataSourceFactory
from core.actors import StrategyActor
from core.commands.ohlcv import IngestMarketData
from core.events.ohlcv import NewMarketDataReceived
from core.models.datasource_type import DataSourceType
from core.models.entity.bar import Bar
from core.models.symbol import Symbol
from core.models.timeframe import Timeframe
from core.models.wss_type import WSType
from core.tasks.feed import StartRealtimeFeed

from .streams.base import AsyncRealTimeData
from .streams.collector import DataCollector
from .streams.strategy import (
    KlineStreamStrategy,
    LiquidationStreamStrategy,
    OrderBookStreamStrategy,
    OrderStreamStrategy,
    PositionStreamStrategy,
)

logger = logging.getLogger(__name__)


class RealtimeActor(StrategyActor):
    def __init__(
        self,
        symbol: Symbol,
        timeframe: Timeframe,
        datasource: DataSourceFactory,
    ):
        super().__init__(symbol, timeframe)
        self.datasource = datasource
        self.collector = DataCollector()

        self.collector.add_producer(self._kline_producer)
        self.collector.add_producer(self._ob_producer)
        self.collector.add_producer(self._liquidation_producer)
        self.collector.add_producer(self._order_producer)
        self.collector.add_producer(self._position_producer)
        self.collector.add_consumer(self._consumer)

        self.depth = 50

    def on_stop(self):
        asyncio.create_task(self.collector.stop())

    async def on_receive(self, msg: StartRealtimeFeed):
        await self.collector.start(msg)

    async def _kline_producer(self, msg: StartRealtimeFeed):
        ws = self.datasource.create(DataSourceType.ExWS, msg.exchange, WSType.PUBLIC)
        async with AsyncRealTimeData(
            ws, KlineStreamStrategy(self.timeframe, self.symbol)
        ) as stream:
            async for bars in stream:
                yield bars

    async def _ob_producer(self, msg: StartRealtimeFeed):
        ws = self.datasource.create(DataSourceType.ExWS, msg.exchange, WSType.PUBLIC)
        async with AsyncRealTimeData(
            ws, OrderBookStreamStrategy(self.symbol, self.depth)
        ) as stream:
            async for orders in stream:
                yield orders

    async def _liquidation_producer(self, msg: StartRealtimeFeed):
        ws = self.datasource.create(DataSourceType.ExWS, msg.exchange, WSType.PUBLIC)
        async with AsyncRealTimeData(
            ws, LiquidationStreamStrategy(self.symbol)
        ) as stream:
            async for liquidations in stream:
                yield liquidations

    async def _order_producer(self, msg: StartRealtimeFeed):
        ws = self.datasource.create(DataSourceType.ExWS, msg.exchange, WSType.PRIVATE)
        async with AsyncRealTimeData(ws, OrderStreamStrategy(self.symbol)) as stream:
            async for order in stream:
                yield order

    async def _position_producer(self, msg: StartRealtimeFeed):
        ws = self.datasource.create(DataSourceType.ExWS, msg.exchange, WSType.PRIVATE)
        async with AsyncRealTimeData(ws, PositionStreamStrategy(self.symbol)) as stream:
            async for position in stream:
                yield position

    async def _consumer(self, data: List[Bar]):
        match data:
            case [Bar(), *_]:
                await self._process_bars(data)

    async def _process_bars(self, bars: List[Bar]):
        for bar in bars:
            await self.ask(IngestMarketData(self.symbol, self.timeframe, bar))
            await self.tell(NewMarketDataReceived(self.symbol, self.timeframe, bar))

            if bar.closed:
                logger.info(f"{self.symbol}_{self.timeframe}:{bar}")
