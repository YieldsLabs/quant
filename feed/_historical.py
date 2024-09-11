import asyncio
from typing import AsyncIterator, List

from core.actors import StrategyActor
from core.commands.feed import StartHistoricalFeed
from core.events.ohlcv import NewMarketDataReceived
from core.interfaces.abstract_config import AbstractConfig
from core.interfaces.abstract_exchange import AbstractExchange
from core.interfaces.abstract_timeseries import AbstractTimeSeriesService
from core.models.bar import Bar
from core.models.lookback import Lookback
from core.models.ohlcv import OHLCV
from core.models.symbol import Symbol
from core.models.timeframe import Timeframe


class AsyncHistoricalData:
    def __init__(
        self,
        exchange: AbstractExchange,
        symbol: Symbol,
        timeframe: Timeframe,
        in_sample: Lookback,
        out_sample: Lookback,
        batch_size: int,
    ):
        self.exchange = exchange
        self.symbol = symbol
        self.timeframe = timeframe
        self.in_sample = in_sample
        self.out_sample = out_sample
        self.batch_size = batch_size
        self.iterator = None
        self.sentinel = object()
        self.last_row = None

    async def __aenter__(self):
        self.iterator = self.exchange.fetch_ohlcv(
            self.symbol,
            self.timeframe,
            self.in_sample,
            self.out_sample,
            self.batch_size,
        )
        return self

    async def __aexit__(self, exc_type, exc_value, traceback):
        self.iterator = None

    def __aiter__(self):
        return self

    async def __anext__(self):
        next_item = await self._fetch_next_item()

        if next_item is self.sentinel:
            raise StopAsyncIteration

        self.last_row = next_item
        return next_item

    async def _fetch_next_item(self):
        return await asyncio.to_thread(self._next_item_or_end)

    def _next_item_or_end(self):
        try:
            return Bar(OHLCV.from_list(next(self.iterator)), True)
        except StopIteration:
            return self.sentinel


class HistoricalActor(StrategyActor):
    def __init__(
        self,
        symbol: Symbol,
        timeframe: Timeframe,
        exchange: AbstractExchange,
        ts: AbstractTimeSeriesService,
        config_service: AbstractConfig,
    ):
        super().__init__(symbol, timeframe)
        self.exchange = exchange
        self.ts = ts
        self.config_service = config_service.get("backtest")
        self.queue = asyncio.Queue()
        self.batch_size = self.config_service["batch_size"]

    async def on_receive(self, msg: StartHistoricalFeed):
        producer = asyncio.create_task(self._producer(msg))
        consumer = asyncio.create_task(self._consumer())

        await asyncio.gather(producer, consumer)

    async def _producer(self, msg: StartHistoricalFeed):
        async with AsyncHistoricalData(
            self.exchange,
            self.symbol,
            self.timeframe,
            msg.in_sample,
            msg.out_sample,
            self.batch_size,
        ) as stream:
            async for batch in self.batched(stream, self.batch_size):
                await self.queue.put(batch)

            await self.queue.put(None)

    async def _consumer(self):
        while True:
            batch = await self.queue.get()

            if batch is None:
                break

            await self._process_batch(batch)
            self.queue.task_done()

    async def _process_batch(self, batch: List[Bar]):
        await self._outbox(batch)
        await self._handle_market(batch)

    async def _handle_market(self, batch: List[Bar]) -> None:
        for bar in batch:
            await self.tell(
                NewMarketDataReceived(
                    self.symbol, self.timeframe, bar.ohlcv, bar.closed
                )
            )
        await asyncio.sleep(0.0001)

    async def _outbox(self, batch: List[Bar]) -> None:
        tasks = [
            self.ts.upsert(self.symbol, self.timeframe, bar.ohlcv)
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
