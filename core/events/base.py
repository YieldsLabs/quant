import uuid
from dataclasses import asdict, dataclass, field
from datetime import datetime
from enum import Enum


class EventGroup(Enum):
    account = "account"
    backtest = "backtest"
    market = "market"
    portfolio = "portfolio"
    position = "position"
    risk = "risk"
    service = "service"
    signal = "signal"

    def __str__(self):
        return self.value


@dataclass
class EventMeta:
    key: str = field(default_factory=lambda: str(uuid.uuid4()))
    timestamp: int = field(default_factory=lambda: datetime.now().timestamp())
    priority: int = field(default_factory=lambda: 0)
    version: int = field(default_factory=lambda: 1)
    group: EventGroup = field(default_factory=lambda: EventGroup.service)


@dataclass(frozen=True)
class Event:
    def to_dict(self):
        res = asdict(self)
        res["meta"]["name"] = self.__class__.__name__
        return res


@dataclass(frozen=True)
class EventEnded(Event):
    meta: EventMeta = field(default_factory=lambda: EventMeta(priority=1))
