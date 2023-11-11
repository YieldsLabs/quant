from dataclasses import dataclass

from core.commands.base import Command


@dataclass(frozen=True)
class PortfolioReset(Command):
    pass
