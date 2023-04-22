from dataclasses import dataclass, field
from datetime import datetime
import uuid


@dataclass(order=True)
class EventMeta:
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    timestamp: int = field(default_factory=lambda: datetime.now().timestamp())
    priority: int = 0

@dataclass
class Event:
    pass
