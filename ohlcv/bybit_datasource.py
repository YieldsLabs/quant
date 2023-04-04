
from typing import Type
from broker.abstract_broker import AbstractBroker
from ohlcv.abstract_datasource import AbstractDatasource


class BybitDataSource(AbstractDatasource):
    def __init__(self, broker: Type[AbstractBroker], lookback=1000):
        self.broker = broker
        self.lookback = lookback

    def fetch(self, symbol: str, timeframe: str):
        return self.broker.get_historical_data(symbol=symbol, timeframe=timeframe, lookback=self.lookback)
