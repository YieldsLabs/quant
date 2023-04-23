import asyncio
from aiocache import cached
from typing import Type
from broker.abstract_broker import AbstractBroker
from datasource.abstract_datasource import AbstractDatasource
from .retry import retry
from core.timeframe import Timeframe


class BybitDataSource(AbstractDatasource):
    def __init__(self, broker: Type[AbstractBroker]):
        self.broker = broker
        self.cache_lock = asyncio.Lock()

    async def _fetch(self, symbol: str, timeframe: Timeframe, lookback=1000):
        return await asyncio.to_thread(self.broker.get_historical_data, symbol, timeframe.value, lookback=lookback)

    async def _account_size(self):
        return await asyncio.to_thread(self.broker.get_account_balance)

    async def _symbols(self):
        return await asyncio.to_thread(self.broker.get_symbols)

    async def _fee_and_precisions(self, symbol):
        return await asyncio.to_thread(self.broker.get_symbol_info, symbol)

    @retry(max_retries=7, initial_retry_delay=3)
    @cached(ttl=100)
    async def fetch(self, symbol: str, timeframe: Timeframe, lookback=1000):
        async with self.cache_lock:
            return await self._fetch(symbol, timeframe, lookback)
    
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