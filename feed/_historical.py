import asyncio
from typing import AsyncIterator, List

from coral import DataSourceFactory
from core.actors import FeedActor
from core.actors.decorators import Consumer, Producer
from core.commands.market import IngestMarketData
from core.events.market import NewMarketDataReceived
from core.interfaces.abstract_config import AbstractConfig
from core.models.datasource_type import DataSourceType
from core.models.entity.bar import Bar
from core.models.entity.ohlcv import OHLCV
from core.models.protocol_type import ProtocolType
from core.models.symbol import Symbol
from core.models.timeframe import Timeframe
from core.tasks.feed import StartHistoricalFeed

from .streams.base import AsyncHistoricalData


class HistoricalActor(FeedActor):
    def __init__(
        self,
        symbol: Symbol,
        timeframe: Timeframe,
        datasource: DataSourceType,
        datasource_factory: DataSourceFactory,
        config_service: AbstractConfig,
    ):
        super().__init__(symbol, timeframe, datasource)
        self.datasource_factory = datasource_factory
        self.config = config_service.get("backtest")

    async def on_receive(self, msg: StartHistoricalFeed):
        await self.collector.start(msg)
        await self.collector.wait_for_completion()

    @Producer
    async def _kline_producer(self, msg: StartHistoricalFeed):
        async with AsyncHistoricalData(
            self.datasource_factory.create(msg.datasource, ProtocolType.REST),
            self.symbol,
            self.timeframe,
            msg.in_sample,
            msg.out_sample,
            self.config.get("batch_size", 100),
            lambda data: Bar(OHLCV.from_list(data), True),
        ) as stream:
            async for batch in self.batched(stream, self.config.get("buff_size", 8)):
                yield batch

    @Consumer
    async def _consumer(self, data: List[Bar]):
        match data:
            case [Bar(), *_]:
                await self._process_batch(data)

    async def _process_batch(self, batch: List[Bar]):
        await self._outbox(batch)
        await self._handle_market(batch)

    async def _handle_market(self, batch: List[Bar]) -> None:
        for bar in batch:
            await self.tell(
                NewMarketDataReceived(self.symbol, self.timeframe, self.datasource, bar)
            )
        await asyncio.sleep(0.0001)

    async def _outbox(self, batch: List[Bar]) -> None:
        tasks = [
            self.ask(
                IngestMarketData(self.symbol, self.timeframe, self.datasource, bar)
            )
            for bar in batch
            if bar.closed
        ]

        await asyncio.gather(*tasks)

    @staticmethod
    async def batched(stream: AsyncIterator[Bar], batch_size: int):
        batch = []
        async for bar in stream:
            batch.append(bar)

            if len(batch) >= batch_size:
                yield batch
                batch = []

        if batch:
            yield batch
