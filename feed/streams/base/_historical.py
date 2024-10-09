import asyncio

from core.interfaces.abstract_exchange import AbstractRestExchange
from core.models.lookback import Lookback
from core.models.symbol import Symbol
from core.models.timeframe import Timeframe


class AsyncHistoricalData:
    def __init__(
        self,
        exchange: AbstractRestExchange,
        symbol: Symbol,
        timeframe: Timeframe,
        in_sample: Lookback,
        out_sample: Lookback,
        batch_size: int,
        parse_fn=None,
    ):
        self.exchange = exchange
        self.symbol = symbol
        self.timeframe = timeframe
        self.in_sample = in_sample
        self.out_sample = out_sample
        self.batch_size = batch_size
        self.iterator = None
        self.sentinel = object()
        self.parse_fn = parse_fn or self._default_parse

    async def __aenter__(self) -> "AsyncHistoricalData":
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

    def __aiter__(self) -> "AsyncHistoricalData":
        return self

    async def __anext__(self):
        next_item = await self._fetch_next_item()

        if next_item is self.sentinel:
            raise StopAsyncIteration

        return next_item

    async def _fetch_next_item(self):
        return await asyncio.to_thread(self._next_item_or_end)

    def _next_item_or_end(self):
        try:
            raw_data = next(self.iterator)
            return self.parse_fn(raw_data)
        except StopIteration:
            return self.sentinel

    def _default_parse(self, raw_data):
        return raw_data
