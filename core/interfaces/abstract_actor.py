from abc import abstractmethod
from typing import Union

from core.events.backtest import BacktestEnded
from core.events.ohlcv import NewMarketDataReceived
from core.events.position import (
    BrokerPositionClosed,
    BrokerPositionOpened,
    PositionClosed,
    PositionCloseRequested,
    PositionInitialized,
    PositionOpened,
)
from core.events.risk import RiskThresholdBreached
from core.events.signal import (
    ExitLongSignalReceived,
    ExitShortSignalReceived,
    GoLongSignalReceived,
    GoShortSignalReceived,
)
from core.models.strategy import Strategy
from core.models.symbol import Symbol
from core.models.timeframe import Timeframe

from .abstract_event_manager import AbstractEventManager

ActorEvent = Union[
    NewMarketDataReceived,
    PositionInitialized,
    PositionOpened,
    PositionClosed,
    BrokerPositionOpened,
    BrokerPositionClosed,
    BacktestEnded,
    PositionCloseRequested,
    GoLongSignalReceived,
    GoShortSignalReceived,
    ExitLongSignalReceived,
    ExitShortSignalReceived,
    RiskThresholdBreached,
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
    def handle(self, event: ActorEvent):
        pass
