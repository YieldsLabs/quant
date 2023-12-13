from dataclasses import dataclass, field

from core.events.base import EventMeta

from .base import Command, CommandGroup


@dataclass(frozen=True)
class AccountCommand(Command):
    meta: EventMeta = field(
        default_factory=lambda: EventMeta(priority=4, group=CommandGroup.account),
        init=False,
    )


@dataclass(frozen=True)
class UpdateAccountSize(AccountCommand):
    amount: float
