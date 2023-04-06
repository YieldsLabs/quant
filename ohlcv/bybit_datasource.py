import time
from typing import Type
from broker.abstract_broker import AbstractBroker
from ohlcv.abstract_datasource import AbstractDatasource
from shared.timeframes import Timeframes
from requests.exceptions import RequestException

class BybitDataSource(AbstractDatasource):
    def __init__(self, broker: Type[AbstractBroker], lookback=1000, max_retries=7, initial_retry_delay=3):
        self.broker = broker
        self.lookback = lookback
        self.max_retries = max_retries
        self.initial_retry_delay = initial_retry_delay

    def fetch(self, symbol: str, timeframe: Timeframes):
        retries = 0

        while retries < self.max_retries:
            try:
                return self.broker.get_historical_data(symbol, timeframe.value, lookback=self.lookback)

            except RequestException as e:
                print(f"Request error: {e}. Retrying...")

            except Exception as e:
                print(f"Unexpected error: {e}. Retrying...")

            retry_delay = self.initial_retry_delay * (2 ** retries)
            print(f"Waiting {retry_delay} seconds before retrying.")
            time.sleep(retry_delay)
            retries += 1

        raise Exception(f"Failed to fetch data for {symbol} after {self.max_retries} retries.")
