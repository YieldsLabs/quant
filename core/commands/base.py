import asyncio
import hashlib
from dataclasses import dataclass, field, fields

from core.events.base import Event, EventMeta


@dataclass(frozen=True)
class Command(Event):
    _execution_event: asyncio.Event = field(default_factory=asyncio.Event, init=False)
    meta: EventMeta = field(default_factory=lambda: EventMeta(priority=1), init=False)

    def executed(self):
        self._execution_event.set()

    async def wait_for_execution(self):
        await self._execution_event.wait()

    def __post_init__(self):
        attribute_values = [
            getattr(self, field.name)
            for field in fields(self)
            if field.name not in ["meta", "_execution_event"]
        ]
        concatenated = f"{self.__class__.__name__}{attribute_values}"
        idempotency_key = hashlib.sha256(concatenated.encode("utf-8")).hexdigest()

        object.__setattr__(self, "meta", EventMeta(priority=1, key=idempotency_key))
