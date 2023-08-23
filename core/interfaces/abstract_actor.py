from abc import abstractmethod

from .abstract_event_manager import AbstractEventManager

from ..models.strategy import Strategy
from ..events.ohlcv import NewMarketDataReceived


class AbstractActor(AbstractEventManager):
    @property
    @abstractmethod
    def strategy(self) -> Strategy:
        pass

    @property
    @abstractmethod
    def running(self) -> bool:
        pass

    @abstractmethod
    def start(self):
        pass

    @abstractmethod
    def stop(self):
        pass

    @abstractmethod
    def next(self, event: NewMarketDataReceived):
        pass
