import asyncio

from core.models.datasource_type import DataSourceType
from core.models.symbol import Symbol
from core.models.timeframe import Timeframe

from ._base import BaseActor
from .collector import DataCollector
from .policy.feed import FeedPolicy


class FeedActor(BaseActor):
    def __init__(
        self, symbol: Symbol, timeframe: Timeframe, datasource: DataSourceType
    ):
        super().__init__()
        self._collector = DataCollector()
        self._symbol = symbol
        self._timeframe = timeframe
        self._datasource = datasource
        self._id = f"{self.symbol}_{self.timeframe}_{self.datasource.name}"

        self._register_producers_and_consumers()

    @property
    def id(self) -> str:
        return self._id

    @property
    def symbol(self) -> "Symbol":
        return self._symbol

    @property
    def timeframe(self) -> "Timeframe":
        return self._timeframe

    @property
    def datasource(self) -> "DataSourceType":
        return self._datasource

    @property
    def collector(self) -> "DataCollector":
        return self._collector

    def on_stop(self):
        asyncio.create_task(self.collector.stop())

    def pre_receive(self, msg) -> bool:
        return FeedPolicy.should_process(self, msg)

    def _register_producers_and_consumers(self):
        for method in [
            getattr(self, func) for func in dir(self) if callable(getattr(self, func))
        ]:
            if hasattr(method, "_is_producer_"):
                self.collector.add_producer(method)

            if hasattr(method, "_is_consumer_"):
                self.collector.add_consumer(method)
