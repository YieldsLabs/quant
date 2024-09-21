from dataclasses import dataclass, field

from core.events._base import EventMeta
from core.groups.command import CommandGroup

from ._base import Command


@dataclass(frozen=True)
class AccountCommand(Command):
    meta: EventMeta = field(
        default_factory=lambda: EventMeta(priority=4, group=CommandGroup.account),
        init=False,
    )


@dataclass(frozen=True)
class UpdateAccountSize(AccountCommand):
    amount: float
