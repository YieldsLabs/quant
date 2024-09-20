from dataclasses import dataclass, field

from core.models.entity.bar import Bar
from core.models.symbol import Symbol
from core.models.timeframe import Timeframe

from .base import Event, EventGroup, EventMeta


@dataclass(frozen=True)
class MarketEvent(Event):
    symbol: Symbol
    timeframe: Timeframe
    meta: EventMeta = field(
        default_factory=lambda: EventMeta(priority=4, group=EventGroup.market),
        init=False,
    )


@dataclass(frozen=True)
class NewMarketDataReceived(MarketEvent):
    bar: Bar

    def to_dict(self):
        parent_dict = super().to_dict()

        current_dict = {
            "symbol": str(self.symbol),
            "timeframe": str(self.timeframe),
            "bar": self.bar.to_dict(),
        }

        return {**parent_dict, **current_dict}
