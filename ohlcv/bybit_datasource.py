
from typing import Type
from broker.abstract_broker import AbstractBroker
from ohlcv.abstract_datasource import AbstractDatasource
from shared.timeframes import Timeframes


class BybitDataSource(AbstractDatasource):
    def __init__(self, broker: Type[AbstractBroker], lookback=1000):
        self.broker = broker
        self.lookback = lookback

    def fetch(self, symbol: str, timeframe: Timeframes):
        return self.broker.get_historical_data(symbol, timeframe.value, lookback=self.lookback)
