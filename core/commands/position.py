from dataclasses import dataclass, field

from core.events._base import EventMeta
from core.groups.command import CommandGroup
from core.models.entity.position import Position

from ._base import Command


@dataclass(frozen=True)
class PositionCommand(Command):
    meta: EventMeta = field(
        default_factory=lambda: EventMeta(priority=1, group=CommandGroup.position),
        init=False,
    )


@dataclass(frozen=True)
class OpenPosition(PositionCommand):
    position: Position


@dataclass(frozen=True)
class ClosePosition(PositionCommand):
    position: Position
