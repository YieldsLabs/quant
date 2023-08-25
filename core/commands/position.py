from dataclasses import dataclass, field

from .base import Command

from ..events.base import EventMeta
from ..models.position import Position


@dataclass(frozen=True)
class PositionCommand(Command):
    position: Position
    meta: EventMeta = field(default_factory=lambda: EventMeta(priority=4), init=False)

@dataclass(frozen=True)
class PositionOpen(PositionCommand):
    pass

@dataclass(frozen=True)
class PositionUpdate(PositionCommand):
    pass

@dataclass(frozen=True)
class PositionClose(PositionCommand):
    pass

@dataclass(frozen=True)
class PositionCloseAll(Command):
    pass