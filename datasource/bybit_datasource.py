import asyncio
from aiocache import cached
from typing import Type

from broker.abstract_broker import AbstractBroker
from datasource.abstract_datasource import AbstractDatasource
from core.timeframe import Timeframe
from .retry import retry


class AsyncHistoricalData:
    def __init__(self, broker, symbol, timeframe, lookback):
        self.broker = broker
        self.symbol = symbol
        self.timeframe = timeframe
        self.lookback = lookback
        self.iterator = None
        self._end_of_iterator = object()
        self.last_row = None

    def __aiter__(self):
        return self

    async def __anext__(self):
        if self.iterator is None:
            self.iterator = self.broker.get_historical_data(self.symbol, self.timeframe, self.lookback)

        next_item = await self._fetch_next_item()
        if next_item is self._end_of_iterator:
            raise StopAsyncIteration

        self.last_row = next_item
        return next_item

    async def _fetch_next_item(self):
        return await asyncio.to_thread(self._next_item_or_end)

    def _next_item_or_end(self):
        try:
            return next(self.iterator)
        except StopIteration:
            return self._end_of_iterator

    def get_last_row(self):
        return self.last_row


class BybitDataSource(AbstractDatasource):
    def __init__(self, broker: Type[AbstractBroker]):
        self.broker = broker
        self.cache_lock = asyncio.Lock()

    async def _account_size(self):
        return await asyncio.to_thread(self.broker.get_account_balance)

    async def _symbols(self):
        return await asyncio.to_thread(self.broker.get_symbols)

    async def _fee_and_precisions(self, symbol):
        return await asyncio.to_thread(self.broker.get_symbol_info, symbol)

    def fetch(self, symbol: str, timeframe: Timeframe, lookback=1000):
        return AsyncHistoricalData(self.broker, symbol, timeframe.value, lookback)

    @retry(max_retries=7, initial_retry_delay=3)
    @cached(ttl=10)
    async def account_size(self):
        async with self.cache_lock:
            return await self._account_size()

    @retry(max_retries=7, initial_retry_delay=3)
    @cached(ttl=300)
    async def symbols(self):
        async with self.cache_lock:
            return await self._symbols()

    @retry(max_retries=7, initial_retry_delay=3)
    @cached(ttl=300)
    async def fee_and_precisions(self, symbol):
        async with self.cache_lock:
            return await self._fee_and_precisions(symbol)
