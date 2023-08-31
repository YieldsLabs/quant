from dataclasses import asdict, dataclass, field
from datetime import datetime
import uuid


@dataclass
class EventMeta:
    key: str = field(default_factory=lambda: str(uuid.uuid4()))
    timestamp: int = field(default_factory=lambda: datetime.now().timestamp())
    priority: int = field(default_factory=lambda: 1)
    version: int = field(default_factory=lambda: 1)


@dataclass(frozen=True)
class Event:
    def to_dict(self):
        return asdict(self)


@dataclass(frozen=True)
class EventEnded(Event):
    meta: EventMeta = field(default_factory=lambda: EventMeta(priority=1))