from dataclasses import dataclass, field

from core.models.entity.signal import Signal

from .base import Event, EventGroup, EventMeta


@dataclass(frozen=True)
class SignalEvent(Event):
    signal: Signal
    meta: EventMeta = field(
        default_factory=lambda: EventMeta(priority=5, group=EventGroup.signal),
        init=False,
    )

    def to_dict(self):
        parent_dict = super().to_dict()

        current_dict = {
            "signal": self.signal.to_dict(),
        }

        return {**parent_dict, **current_dict}


@dataclass(frozen=True)
class GoLongSignalReceived(SignalEvent):
    pass


@dataclass(frozen=True)
class GoShortSignalReceived(SignalEvent):
    pass


@dataclass(frozen=True)
class ExitLongSignalReceived(SignalEvent):
    pass


@dataclass(frozen=True)
class ExitShortSignalReceived(SignalEvent):
    pass
