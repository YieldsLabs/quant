import asyncio
from typing import AsyncIterator, List

from core.actors import StrategyActor
from core.commands.ohlcv import IngestMarketData
from core.events.ohlcv import NewMarketDataReceived
from core.interfaces.abstract_config import AbstractConfig
from core.interfaces.abstract_exchange import AbstractExchange
from core.models.entity.bar import Bar
from core.models.entity.ohlcv import OHLCV
from core.models.symbol import Symbol
from core.models.timeframe import Timeframe
from core.tasks.feed import StartHistoricalFeed

from .streams.base import AsyncHistoricalData
from .streams.collector import DataCollector


class HistoricalActor(StrategyActor):
    def __init__(
        self,
        symbol: Symbol,
        timeframe: Timeframe,
        exchange: AbstractExchange,
        config_service: AbstractConfig,
    ):
        super().__init__(symbol, timeframe)
        self.exchange = exchange
        self.collector = DataCollector()

        self.collector.add_producer(self._kline_producer)
        self.collector.add_consumer(self._consumer)

        self.config_service = config_service.get("backtest")
        self.batch_size = self.config_service["batch_size"]
        self.buff_size = self.config_service["buff_size"]

    async def on_receive(self, msg: StartHistoricalFeed):
        await self.collector.start(msg)
        await self.collector.wait_for_completion()

    async def _kline_producer(self, msg: StartHistoricalFeed):
        async with AsyncHistoricalData(
            self.exchange,
            self.symbol,
            self.timeframe,
            msg.in_sample,
            msg.out_sample,
            self.batch_size,
            lambda data: Bar(OHLCV.from_list(data), True),
        ) as stream:
            async for batch in self.batched(stream, self.buff_size):
                yield batch

    async def _consumer(self, data: List[Bar]):
        match data:
            case [Bar(), *_]:
                await self._process_batch(data)

    async def _process_batch(self, batch: List[Bar]):
        await self._outbox(batch)
        await self._handle_market(batch)

    async def _handle_market(self, batch: List[Bar]) -> None:
        for bar in batch:
            await self.tell(NewMarketDataReceived(self.symbol, self.timeframe, bar))
        await asyncio.sleep(0.0001)

    async def _outbox(self, batch: List[Bar]) -> None:
        tasks = [
            self.ask(IngestMarketData(self.symbol, self.timeframe, bar))
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
