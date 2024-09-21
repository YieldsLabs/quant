from dataclasses import dataclass, field

from core.events._base import EventMeta
from core.groups.tasks import TasksGroup
from core.models.lookback import Lookback
from core.models.symbol import Symbol
from core.models.timeframe import Timeframe

from ._base import Task


@dataclass(frozen=True)
class FeedTask(Task):
    symbol: Symbol
    timeframe: Timeframe
    meta: EventMeta = field(
        default_factory=lambda: EventMeta(priority=2, group=TasksGroup.feed),
        init=False,
    )


@dataclass(frozen=True)
class StartHistoricalFeed(FeedTask):
    in_sample: Lookback
    out_sample: Lookback | None


@dataclass(frozen=True)
class StartRealtimeFeed(FeedTask):
    pass
