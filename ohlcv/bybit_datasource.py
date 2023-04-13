from typing import Type
from broker.abstract_broker import AbstractBroker
from ohlcv.abstract_datasource import AbstractDatasource
from shared.retry import retry
from shared.timeframes import Timeframes
from cachetools import TTLCache, cached


class BybitDataSource(AbstractDatasource):
    def __init__(self, broker: Type[AbstractBroker], lookback=1000):
        self.broker = broker
        self.lookback = lookback

    @retry(max_retries=7, initial_retry_delay=3)
    @cached(cache=TTLCache(maxsize=5000, ttl=8))
    def fetch(self, symbol: str, timeframe: Timeframes):
        return self.broker.get_historical_data(symbol, timeframe.value, lookback=self.lookback)
