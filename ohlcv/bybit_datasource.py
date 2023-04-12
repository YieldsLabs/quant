import random
import time
from typing import Type
from broker.abstract_broker import AbstractBroker
from ohlcv.abstract_datasource import AbstractDatasource
from shared.timeframes import Timeframes
from requests.exceptions import RequestException
from cachetools import TTLCache, cached


class BybitDataSource(AbstractDatasource):
    def __init__(self, broker: Type[AbstractBroker], lookback=1000, max_retries=7, initial_retry_delay=3):
        self.broker = broker
        self.lookback = lookback
        self.max_retries = max_retries
        self.initial_retry_delay = initial_retry_delay

    @cached(cache=TTLCache(maxsize=5000, ttl=8))
    def fetch(self, symbol: str, timeframe: Timeframes):
        return self._retry(
            self.broker.get_historical_data,
            symbol,
            timeframe.value,
            lookback=self.lookback,
        )

    def _retry(self, function, *args, **kwargs):
        retries = 0
        while retries < self.max_retries:
            try:
                return function(*args, **kwargs)
            except (RequestException, Exception) as e:
                print(f"Error: {e}. Retrying...")
                retries += 1
                retry_delay = self.initial_retry_delay * (2 ** retries) * random.uniform(0.5, 1.5)
                print(f"Waiting {retry_delay} seconds before retrying.")
                time.sleep(retry_delay)

        raise Exception("Failed to fetch data after reaching maximum retries.")
