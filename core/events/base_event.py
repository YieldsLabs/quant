from dataclasses import dataclass, field
from datetime import datetime
import uuid


@dataclass
class EventMeta:
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    timestamp: int = field(default_factory=lambda: datetime.now().timestamp())
    priority: int = field(default_factory=lambda: 1)


@dataclass(frozen=True)
class Event:
    pass


@dataclass(frozen=True)
class EndEvent(Event):
    meta: EventMeta = field(default_factory=lambda: EventMeta(priority=1))
