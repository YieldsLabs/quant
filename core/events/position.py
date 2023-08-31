from dataclasses import dataclass, field

from .base import Event, EventGroup, EventMeta

from ..models.position import Position


@dataclass(frozen=True)
class PositionEvent(Event):
    position: Position
    meta: EventMeta = field(default_factory=lambda: EventMeta(priority=2, group=EventGroup.position), init=False)


@dataclass(frozen=True)
class PositionInitialized(PositionEvent):
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
