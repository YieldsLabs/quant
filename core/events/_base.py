from dataclasses import asdict, dataclass, field

from core.events.meta import EventMeta


@dataclass(frozen=True)
class Event:
    meta: EventMeta

    def to_dict(self):
        res = asdict(self)
        res["meta"]["name"] = self.__class__.__name__
        return res


@dataclass(frozen=True)
class EventEnded(Event):
    meta: EventMeta = field(default_factory=lambda: EventMeta(priority=1))
