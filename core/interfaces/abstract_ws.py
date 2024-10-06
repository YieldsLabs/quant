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
    def auth(self):
        pass

    @abstractmethod
    def subscribe(self, topic: str):
        pass

    @abstractmethod
    def get_message(self):
        pass

    @abstractmethod
    def unsubscribe(self, topic: str):
        pass

    @abstractmethod
    def kline_topic(self, timeframe: Timeframe, symbol: Symbol):
        pass

    @abstractmethod
    def order_book_topic(self, symbol: Symbol, depth: int):
        pass

    @abstractmethod
    def liquidation_topic(self, symbol: Symbol):
        pass

    @abstractmethod
    def order_topic(self):
        pass

    @abstractmethod
    def position_topic(self):
        pass
