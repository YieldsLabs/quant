from dataclasses import dataclass, field

from core.events._base import EventMeta
from core.groups.command import CommandGroup
from core.models.broker import MarginMode, PositionMode
from core.models.datasource_type import DataSourceType
from core.models.symbol import Symbol

from ._base import Command


@dataclass(frozen=True)
class BrokerCommand(Command):
    meta: EventMeta = field(
        default_factory=lambda: EventMeta(priority=5, group=CommandGroup.broker),
        init=False,
    )


@dataclass(frozen=True)
class UpdateSymbolSettings(BrokerCommand):
    datasource: DataSourceType
    symbol: Symbol
    leverage: int
    position_mode: PositionMode
    margin_mode: MarginMode
