from abc import abstractmethod
from typing import Union

from .abstract_event_manager import AbstractEventManager

from ..events.position import PositionInitialized, PositionClosed
from ..events.ohlcv import NewMarketDataReceived


ActorEvent = Union[NewMarketDataReceived, PositionInitialized, PositionClosed]

class AbstractActor(AbstractEventManager):
    @property
    @abstractmethod
    def id(self) -> str:
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
    def handle(self, event: ActorEvent):
        pass
