from dataclasses import dataclass, field

from core.events._base import EventMeta
from core.groups.command import CommandGroup

from ._base import Command


@dataclass(frozen=True)
class PortfolioCommand(Command):
    meta: EventMeta = field(
        default_factory=lambda: EventMeta(priority=3, group=CommandGroup.portfolio),
        init=False,
    )


@dataclass(frozen=True)
class PortfolioReset(PortfolioCommand):
    pass


@dataclass(frozen=True)
class StrategyReset(PortfolioCommand):
    pass
