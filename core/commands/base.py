import asyncio
from dataclasses import dataclass, field

from ..events.base import Event, EventMeta


@dataclass(frozen=True)
class Command(Event):
    _execution_event: asyncio.Event = field(default_factory=asyncio.Event, init=False)
    meta: EventMeta = field(default_factory=lambda: EventMeta(priority=1), init=False)

    def executed(self):
        self._execution_event.set()

    async def wait_for_execution(self):
        await self._execution_event.wait()