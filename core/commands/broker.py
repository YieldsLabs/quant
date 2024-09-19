from dataclasses import dataclass, field

from core.events.base import EventMeta
from core.models.broker import MarginMode, PositionMode
from core.models.entity.position import Position
from core.models.symbol import Symbol

from .base import Command, CommandGroup


@dataclass(frozen=True)
class BrokerCommand(Command):
    meta: EventMeta = field(
        default_factory=lambda: EventMeta(priority=1, group=CommandGroup.broker),
        init=False,
    )


@dataclass(frozen=True)
class UpdateSettings(BrokerCommand):
    symbol: Symbol
    leverage: int
    position_mode: PositionMode
    margin_mode: MarginMode


@dataclass(frozen=True)
class OpenPosition(BrokerCommand):
    position: Position


@dataclass(frozen=True)
class ClosePosition(BrokerCommand):
    position: Position
