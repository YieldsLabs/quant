from dataclasses import dataclass, field

from core.commands.base import Command, CommandGroup
from core.events.base import EventMeta


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
