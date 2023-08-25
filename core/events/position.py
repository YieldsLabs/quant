from dataclasses import dataclass, field

from .base import Event, EventMeta

from ..models.position import Position


@dataclass(frozen=True)
class PositionEvent(Event):
    position: Position
    meta: EventMeta = field(default_factory=lambda: EventMeta(priority=2))


@dataclass(frozen=True)
class LongPositionOpened(PositionEvent):
    pass


@dataclass(frozen=True)
class ShortPositionOpened(PositionEvent):
    pass


@dataclass(frozen=True)
class PositionClosed(Event):
    position: Position
    meta: EventMeta = field(default_factory=lambda: EventMeta(priority=4))