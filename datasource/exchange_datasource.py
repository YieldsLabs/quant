import asyncio

from core.interfaces.abstract_datasource import AbstractDataSource
from core.interfaces.abstract_exchange import AbstractExchange
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

    def __aiter__(self):
        return self

    async def __anext__(self):
        self._init_iterator()

        next_item = await self._fetch_next_item()
        if next_item is self.sentinel:
            raise StopAsyncIteration

        self.last_row = next_item
        return next_item

    def _init_iterator(self) -> None:
        if self.iterator is None:
            self.iterator = self.exchange.fetch_ohlcv(
                self.symbol,
                self.timeframe,
                self.in_sample,
                self.out_sample,
                self.batch_size,
            )

    async def _fetch_next_item(self):
        return await asyncio.to_thread(self._next_item_or_end)

    def _next_item_or_end(self):
        try:
            return OHLCV.from_list(next(self.iterator))
        except StopIteration:
            return self.sentinel

    def get_last_row(self):
        return self.last_row


class ExchangeDataSource(AbstractDataSource):
    def __init__(
        self, exchange: AbstractExchange, symbol: Symbol, timeframe: Timeframe
    ):
        super().__init__()
        self.exchange = exchange
        self.symbol = symbol
        self.timeframe = timeframe

    def fetch(
        self,
        in_sample: Lookback,
        out_sample: Lookback,
        batch_size: int,
    ):
        return AsyncHistoricalData(
            self.exchange,
            self.symbol,
            self.timeframe,
            in_sample,
            out_sample,
            batch_size,
        )
