import asyncio

from cachetools import TTLCache

from core.events.base import Event


class EventDedup:
    def __init__(self, ttl: int = 10, maxsize: int = 2048):
        self._events_in_queue = TTLCache(maxsize=maxsize, ttl=ttl)
        self._lock = asyncio.Lock()

    async def acquire(self, event: Event) -> bool:
        async with self._lock:
            key = event.meta.key
            if key in self._events_in_queue:
                return False
            self._events_in_queue[key] = True
            return True

    async def release(self, event: Event) -> None:
        async with self._lock:
            self._events_in_queue.pop(event.meta.key, None)
