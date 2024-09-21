import uuid
from dataclasses import dataclass, field
from datetime import datetime

from core.groups.event import EventGroup


@dataclass
class EventMeta:
    key: str = field(default_factory=lambda: str(uuid.uuid4()))
    timestamp: int = field(default_factory=lambda: datetime.now().timestamp())
    priority: int = field(default_factory=lambda: 0)
    version: int = field(default_factory=lambda: 1)
    group: EventGroup = field(default_factory=lambda: EventGroup.service)
