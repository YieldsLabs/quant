from abc import ABC, abstractmethod
from typing import Union

from core.commands._base import Command
from core.commands.market import IngestMarketData
from core.events.backtest import BacktestEnded
from core.events.market import NewMarketDataReceived, NewMarketOrderReceived
from core.events.position import (
    BrokerPositionClosed,
    BrokerPositionOpened,
    PositionClosed,
    PositionCloseRequested,
    PositionInitialized,
    PositionOpened,
)
from core.events.risk import RiskLongThresholdBreached, RiskShortThresholdBreached
from core.events.signal import (
    ExitLongSignalReceived,
    ExitShortSignalReceived,
    GoLongSignalReceived,
    GoShortSignalReceived,
)
from core.queries._base import Query
from core.queries.ohlcv import TA, BackNBars, BatchBars, NextBar, PrevBar
from core.tasks.feed import StartHistoricalFeed, StartRealtimeFeed

Message = Union[
    NewMarketDataReceived,
    NewMarketOrderReceived,
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
    RiskLongThresholdBreached,
    RiskShortThresholdBreached,
    StartHistoricalFeed,
    StartRealtimeFeed,
    IngestMarketData,
    NextBar,
    PrevBar,
    BatchBars,
    BackNBars,
    TA,
]

Ask = Union[Command, Query]


class AbstractActor(ABC):
    @property
    @abstractmethod
    def id(self) -> str:
        pass

    @property
    @abstractmethod
    def running(self) -> bool:
        pass

    @abstractmethod
    def on_start(self):
        pass

    @abstractmethod
    def on_stop(self):
        pass

    @abstractmethod
    def start(self):
        pass

    @abstractmethod
    def stop(self):
        pass

    @abstractmethod
    def pre_receive(self, msg: Message) -> bool:
        pass

    @abstractmethod
    def on_receive(self, msg: Message):
        pass

    @abstractmethod
    def tell(self, msg: Message):
        pass

    @abstractmethod
    def ask(self, ask: Ask):
        pass
