import asyncio
from aiocache import cached, SimpleMemoryCache
from aiocache.serializers import JsonSerializer
from typing import Type
from broker.abstract_broker import AbstractBroker
from datasource.abstract_datasource import AbstractDatasource
from .retry import retry
from core.timeframe import Timeframe

cache = SimpleMemoryCache(serializer=JsonSerializer())

class BybitDataSource(AbstractDatasource):
    def __init__(self, broker: Type[AbstractBroker]):
        self.broker = broker

    @retry(max_retries=7, initial_retry_delay=3)
    async def fetch(self, symbol: str, timeframe: Timeframe, lookback=1000):
       return await asyncio.to_thread(self.broker.get_historical_data, symbol, timeframe.value, lookback=lookback)
    
    @retry(max_retries=7, initial_retry_delay=3)
    async def account_size(self):
        return await asyncio.to_thread(self.broker.get_account_balance)
    
    @retry(max_retries=7, initial_retry_delay=3)
    async def symbols(self):
        return await asyncio.to_thread(self.broker.get_symbols)
    
    @retry(max_retries=7, initial_retry_delay=3)
    async def fee_and_precisions(self, symbol):
        return await asyncio.to_thread(self.broker.get_symbol_info, symbol)