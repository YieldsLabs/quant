import asyncio
from typing import Set

from core.events.base import Event


class EventDedup:
    def __init__(self):
        self._events_in_queue: Set[int] = set()
        self._lock = asyncio.Lock()

    async def add_event(self, event: Event) -> bool:
        async with self._lock:
            key = event.meta.key

            if key in self._events_in_queue:
                return False

            self._events_in_queue.add(key)

            return True

    async def remove_event(self, event: Event) -> None:
        async with self._lock:
            self._events_in_queue.discard(event.meta.key)
