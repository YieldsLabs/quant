from dataclasses import dataclass, field

from core.models.ohlcv import OHLCV

from .base import Event, EventMeta

from ..models.signal import Signal


@dataclass(frozen=True)
class SignalEntryEvent(Event):
    signal: Signal
    entry_price: float
    stop_loss: float
    ohlcv: OHLCV
    meta: EventMeta = field(default_factory=lambda: EventMeta(priority=6))


@dataclass(frozen=True)
class SignalExitEvent(Event):
    signal: Signal
    exit_price: float
    ohlcv: OHLCV
    meta: EventMeta = field(default_factory=lambda: EventMeta(priority=1))


@dataclass(frozen=True)
class GoLongSignalReceived(SignalEntryEvent):
    pass


@dataclass(frozen=True)
class GoShortSignalReceived(SignalEntryEvent):
    pass


@dataclass(frozen=True)
class ExitLongSignalReceived(SignalExitEvent):
    pass


@dataclass(frozen=True)
class ExitShortSignalReceived(SignalExitEvent):
    pass
