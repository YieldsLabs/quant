from dataclasses import asdict, dataclass, field

from core.models.ohlcv import OHLCV

from .base import Event, EventGroup, EventMeta

from ..models.signal import Signal


@dataclass(frozen=True)
class SignalEvent(Event):
    signal: Signal
    meta: EventMeta = field(default_factory=lambda: EventMeta(priority=5, group=EventGroup.signal), init=False)


@dataclass(frozen=True)
class SignalEntryEvent(SignalEvent):
    entry_price: float
    stop_loss: float
    ohlcv: OHLCV

    def to_dict(self):
        return {
            'signal': self.signal.to_dict(),
            'entry_price': self.entry_price,
            'stop_loss': self.stop_loss,
            'ohlcv': asdict(self.ohlcv),
            'meta': asdict(self.meta)
        }



@dataclass(frozen=True)
class SignalExitEvent(SignalEvent):
    exit_price: float
    ohlcv: OHLCV

    def to_dict(self):
        return {
            'signal': self.signal.to_dict(),
            'exit_price': self.exit_price,
            'ohlcv': asdict(self.ohlcv),
            'meta': asdict(self.meta)
        }


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
