from dataclasses import dataclass, field

from core.events.meta import EventMeta
from core.groups.event import EventGroup
from core.models.datasource_type import DataSourceType
from core.models.entity.bar import Bar
from core.models.entity.order import Order
from core.models.symbol import Symbol
from core.models.timeframe import Timeframe

from ._base import Event


@dataclass(frozen=True)
class MarketEvent(Event):
    symbol: Symbol
    timeframe: Timeframe
    datasource: DataSourceType
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
            "datasource": str(self.datasource),
            "bar": self.bar.to_dict(),
        }

        return {**parent_dict, **current_dict}


@dataclass(frozen=True)
class NewMarketOrderReceived(MarketEvent):
    order: Order

    def to_dict(self):
        parent_dict = super().to_dict()

        current_dict = {
            "symbol": str(self.symbol),
            "timeframe": str(self.timeframe),
            "datasource": str(self.datasource),
            "order": self.order.to_dict(),
        }

        return {**parent_dict, **current_dict}
