from dataclasses import dataclass, field

from core.commands.base import Command, CommandGroup
from core.events.base import EventMeta
from core.models.lookback import Lookback
from core.models.symbol import Symbol
from core.models.timeframe import Timeframe


@dataclass(frozen=True)
class FeedCommand(Command):
    symbol: Symbol
    timeframe: Timeframe
    meta: EventMeta = field(
        default_factory=lambda: EventMeta(priority=2, group=CommandGroup.feed),
        init=False,
    )


@dataclass(frozen=True)
class StartHistoricalFeed(FeedCommand):
    in_sample: Lookback
    out_sample: Lookback | None


@dataclass(frozen=True)
class StartRealtimeFeed(FeedCommand):
    pass
