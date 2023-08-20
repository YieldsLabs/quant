from dataclasses import dataclass, field

from .base_event import Event, EventMeta
from ..timeframe import Timeframe


@dataclass(frozen=True)
class StrategyEntryEvent(Event):
    symbol: str
    timeframe: Timeframe
    strategy: str
    entry: float
    stop_loss: float
    meta: EventMeta = field(default_factory=lambda: EventMeta(priority=1))


@dataclass(frozen=True)
class StrategyExitEvent(Event):
    symbol: str
    timeframe: Timeframe
    strategy: str
    exit: float
    meta: EventMeta = field(default_factory=lambda: EventMeta(priority=2))


@dataclass(frozen=True)
class GoLongSignalReceived(StrategyEntryEvent):
    pass


@dataclass(frozen=True)
class GoShortSignalReceived(StrategyEntryEvent):
    pass


@dataclass(frozen=True)
class ExitLongSignalReceived(StrategyExitEvent):
    pass


@dataclass(frozen=True)
class ExitShortSignalReceived(StrategyExitEvent):
    pass
