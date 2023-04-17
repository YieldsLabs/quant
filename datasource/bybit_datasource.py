from typing import Type
from broker.abstract_broker import AbstractBroker
from datasource.abstract_datasource import AbstractDatasource
from .retry import retry
from core.timeframes import Timeframes
from cachetools import TTLCache, cached


class BybitDataSource(AbstractDatasource):
    def __init__(self, broker: Type[AbstractBroker]):
        self.broker = broker

    @retry(max_retries=7, initial_retry_delay=3)
    @cached(cache=TTLCache(maxsize=5000, ttl=8))
    def fetch(self, symbol: str, timeframe: Timeframes, lookback=1000):
        return self.broker.get_historical_data(symbol, timeframe.value, lookback=lookback)
    
    @retry(max_retries=7, initial_retry_delay=3)
    @cached(cache=TTLCache(maxsize=100, ttl=10))
    def account_size(self):
        return self.broker.get_account_balance()
    
    @retry(max_retries=7, initial_retry_delay=3)
    @cached(cache=TTLCache(maxsize=1000, ttl=300))
    def symbols(self):
        return self.broker.get_symbols()
    
    @retry(max_retries=7, initial_retry_delay=3)
    @cached(cache=TTLCache(maxsize=100, ttl=300))
    def fee_and_precisions(self, symbol):
        return self.broker.get_symbol_info(symbol)
