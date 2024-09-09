from dataclasses import dataclass, field

from core.models.position import Position

from .base import Event, EventGroup, EventMeta


@dataclass(frozen=True)
class PositionEvent(Event):
    position: Position
    meta: EventMeta = field(
        default_factory=lambda: EventMeta(priority=2, group=EventGroup.position),
        init=False,
    )

    def to_dict(self):
        parent_dict = super().to_dict()

        current_dict = {
            "position": self.position.to_dict(),
        }

        return {**parent_dict, **current_dict}


@dataclass(frozen=True)
class PositionInitialized(PositionEvent):
    pass


@dataclass(frozen=True)
class PositionAdjusted(PositionEvent):
    pass


@dataclass(frozen=True)
class PositionOpened(PositionEvent):
    pass


@dataclass(frozen=True)
class PositionCloseRequested(PositionEvent):
    pass


@dataclass(frozen=True)
class PositionClosed(PositionEvent):
    pass


@dataclass(frozen=True)
class BrokerPositionOpened(PositionEvent):
    pass


@dataclass(frozen=True)
class BrokerPositionReduced(PositionEvent):
    pass


@dataclass(frozen=True)
class BrokerPositionClosed(PositionEvent):
    pass
