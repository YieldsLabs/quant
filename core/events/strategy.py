from dataclasses import dataclass, field

from .base_event import Event, EventMeta

from ..models.strategy import Strategy


@dataclass(frozen=True)
class StrategyEntryEvent(Event):
    strategy: Strategy
    entry: float
    stop_loss: float
    meta: EventMeta = field(default_factory=lambda: EventMeta(priority=5))


@dataclass(frozen=True)
class StrategyExitEvent(Event):
    strategy: Strategy
    exit: float
    meta: EventMeta = field(default_factory=lambda: EventMeta(priority=6))


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
