from dataclasses import dataclass, field

from core.events._base import EventMeta
from core.groups.command import CommandGroup
from core.models.cap import CapType
from core.models.datasource_type import DataSourceType

from ._base import Command


@dataclass(frozen=True)
class FactorCommand(Command):
    meta: EventMeta = field(
        default_factory=lambda: EventMeta(priority=6, group=CommandGroup.factor),
        init=False,
    )


@dataclass(frozen=True)
class InitGeneration(FactorCommand):
    datasource: DataSourceType
    cap: CapType


@dataclass(frozen=True)
class EnvolveGeneration(FactorCommand):
    datasource: DataSourceType
    cap: CapType
