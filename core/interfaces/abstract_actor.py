from abc import abstractmethod
from typing import Union


from .abstract_event_manager import AbstractEventManager

from ..events.signal import ExitLongSignalReceived, ExitShortSignalReceived, GoLongSignalReceived, GoShortSignalReceived
from ..events.position import PositionCloseRequested, PositionInitialized
from ..events.ohlcv import NewMarketDataReceived
from ..events.risk import RiskThresholdBreached
from ..models.symbol import Symbol
from ..models.timeframe import Timeframe


ActorEvent = Union[
    NewMarketDataReceived,
    PositionInitialized,
    PositionCloseRequested,
    GoLongSignalReceived,
    GoShortSignalReceived,
    ExitLongSignalReceived,
    ExitShortSignalReceived,
    RiskThresholdBreached
]

class AbstractActor(AbstractEventManager):
    @property
    @abstractmethod
    def id(self) -> str:
        pass

    @property
    @abstractmethod
    def symbol(self) -> Symbol:
        pass

    @property
    @abstractmethod
    def timeframe(self) -> Timeframe:
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
