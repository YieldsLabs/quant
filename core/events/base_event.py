from dataclasses import dataclass, field
from datetime import datetime
import uuid


@dataclass
class EventMeta:
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    timestamp: int = field(default_factory=lambda: datetime.now().timestamp())
    priority: int = field(default_factory=lambda: 1)

@dataclass
class Event:
    pass
