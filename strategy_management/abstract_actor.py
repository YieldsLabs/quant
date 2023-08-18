from abc import abstractmethod

from core.abstract_event_manager import AbstractEventManager
from core.events.ohlcv import OHLCV


class AbsctractActor(AbstractEventManager):
    @property
    @abstractmethod
    def id(self) -> str:
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
