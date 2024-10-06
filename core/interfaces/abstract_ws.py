from abc import ABC, abstractmethod

from core.models.symbol import Symbol
from core.models.timeframe import Timeframe


class AbstractWS(ABC):
    @abstractmethod
    def connect(self):
        pass

    @abstractmethod
    def close(self):
        pass

    @abstractmethod
    def receive(self):
        pass

    @abstractmethod
    def subscribe(self, topic: str):
        pass

    @abstractmethod
    def unsubscribe(self, topic: str):
        pass

    def kline_topic(self, timeframe: Timeframe, symbol: Symbol):
        pass

    def order_book_topic(self, symbol: Symbol, depth: int):
        pass

    def liquidation_topic(self, symbol: Symbol):
        pass
