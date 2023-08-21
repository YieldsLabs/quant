from abc import abstractmethod

from .abstract_event_manager import AbstractEventManager

from ..models.ohlcv import OHLCV


class AbstractActor(AbstractEventManager):
    @property
    @abstractmethod
    def id(self) -> str:
        pass

    @property
    @abstractmethod
    def strategy(self) -> str:
        pass

    @property
    @abstractmethod
    def symbol(self) -> str:
        pass

    @property
    @abstractmethod
    def timeframe(self) -> str:
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
    def next(self, data: OHLCV):
        pass
