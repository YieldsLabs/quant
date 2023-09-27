from dataclasses import dataclass, field

from .base import Event, EventGroup, EventMeta


@dataclass(frozen=True)
class AccountUpdated(Event):
    amount: float
    meta: EventMeta = field(
        default_factory=lambda: EventMeta(priority=7, group=EventGroup.account),
        init=False,
    )


@dataclass(frozen=True)
class PortfolioAccountUpdated(AccountUpdated):
    pass


@dataclass(frozen=True)
class PositionAccountUpdated(AccountUpdated):
    pass
