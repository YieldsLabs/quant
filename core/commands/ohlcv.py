from dataclasses import dataclass, field

from core.events.meta import EventMeta
from core.groups.command import CommandGroup
from core.models.entity.bar import Bar
from core.models.symbol import Symbol
from core.models.timeframe import Timeframe

from ._base import Command


@dataclass(frozen=True)
class MarketCommand(Command):
    symbol: Symbol
    timeframe: Timeframe
    meta: EventMeta = field(
        default_factory=lambda: EventMeta(priority=2, group=CommandGroup.market),
        init=False,
    )


@dataclass(frozen=True)
class IngestMarketData(MarketCommand):
    bar: Bar
