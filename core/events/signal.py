from dataclasses import asdict, dataclass, field

from core.models.ohlcv import OHLCV
from core.models.signal import Signal

from .base import Event, EventGroup, EventMeta


@dataclass(frozen=True)
class SignalEvent(Event):
    signal: Signal
    ohlcv: OHLCV
    meta: EventMeta = field(
        default_factory=lambda: EventMeta(priority=5, group=EventGroup.signal),
        init=False,
    )


@dataclass(frozen=True)
class SignalEntryEvent(SignalEvent):
    entry_price: float
    stop_loss: float

    def to_dict(self):
        parent_dict = super().to_dict()

        current_dict = {
            "signal": self.signal.to_dict(),
            "entry_price": self.entry_price,
            "stop_loss": self.stop_loss,
            "ohlcv": asdict(self.ohlcv),
        }

        return {**parent_dict, **current_dict}


@dataclass(frozen=True)
class SignalExitEvent(SignalEvent):
    exit_price: float

    def to_dict(self):
        return {
            "signal": self.signal.to_dict(),
            "exit_price": self.exit_price,
            "ohlcv": asdict(self.ohlcv),
            "meta": asdict(self.meta),
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
