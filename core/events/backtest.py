from dataclasses import dataclass, field

from core.events.meta import EventMeta
from core.groups.event import EventGroup
from core.models.strategy import Strategy
from core.models.symbol import Symbol
from core.models.timeframe import Timeframe

from ._base import Event


@dataclass(frozen=True)
class BacktestEvent(Event):
    symbol: Symbol
    timeframe: Timeframe
    strategy: Strategy
    meta: EventMeta = field(
        default_factory=lambda: EventMeta(priority=6, group=EventGroup.backtest),
        init=False,
    )


@dataclass(frozen=True)
class BacktestStarted(BacktestEvent):
    pass


@dataclass(frozen=True)
class BacktestEnded(BacktestEvent):
    pass
