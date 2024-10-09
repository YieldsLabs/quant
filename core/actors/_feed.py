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
        self._tasks = set()

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
        task = asyncio.create_task(self.collector.stop())
        self._tasks.add(task)
        task.add_done_callback(self._tasks.discard)

    def pre_receive(self, msg) -> bool:
        return FeedPolicy.should_process(self, msg)

    def _register_producers_and_consumers(self):
        methods = [
            getattr(self, method_name)
            for method_name in dir(self)
            if callable(getattr(self, method_name))
        ]

        producers = [
            method for method in methods if getattr(method, "_is_producer_", False)
        ]
        consumers = [
            method for method in methods if getattr(method, "_is_consumer_", False)
        ]

        for producer in producers:
            self.collector.add_producer(producer)

        for consumer in consumers:
            self.collector.add_consumer(consumer)
