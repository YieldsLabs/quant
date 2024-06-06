import asyncio
import bisect
from typing import AsyncIterator, List

from core.actors import StrategyActor
from core.commands.feed import StartHistoricalFeed
from core.events.ohlcv import NewMarketDataReceived
from core.interfaces.abstract_config import AbstractConfig
from core.interfaces.abstract_exchange import AbstractExchange
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

    def get_last_bar(self):
        return self.last_row


class HistoricalActor(StrategyActor):
    _EVENTS = [StartHistoricalFeed]

    def __init__(
        self,
        symbol: Symbol,
        timeframe: Timeframe,
        exchange: AbstractExchange,
        config_service: AbstractConfig,
    ):
        super().__init__(symbol, timeframe)
        self.exchange = exchange
        self.config_service = config_service.get("backtest")
        self.buffer: List[Bar] = []

    async def on_receive(self, msg: StartHistoricalFeed):
        symbol, timeframe = msg.symbol, msg.timeframe

        async with AsyncHistoricalData(
            self.exchange,
            symbol,
            timeframe,
            msg.in_sample,
            msg.out_sample,
            self.config_service["batch_size"],
        ) as stream:
            async for bars in self.batched(stream, self.config_service["buff_size"]):
                self._update_buffer(bars)
                await self._process_buffer()

    def _update_buffer(self, batch: List[Bar]):
        for bar in batch:
            bisect.insort(self.buffer, bar, key=lambda x: x.ohlcv.timestamp)

    async def _process_buffer(self):
        buff_size = self.config_service["buff_size"]

        while len(self.buffer) >= buff_size:
            bars = [self.buffer.pop(0) for _ in range(buff_size)]
            await self._handle_market(bars)

    async def _handle_market(self, bars: List[Bar]) -> None:
        for bar in bars:
            await self.tell(
                NewMarketDataReceived(
                    self.symbol, self.timeframe, bar.ohlcv, bar.closed
                )
            )
        await asyncio.sleep(0.00001)

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
