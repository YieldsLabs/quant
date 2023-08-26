from dataclasses import dataclass

from .base import Command

from ..models.position import Position


@dataclass(frozen=True)
class PositionCommand(Command):
    position: Position

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