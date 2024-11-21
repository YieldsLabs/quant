import asyncio
import hashlib

from cachetools import TTLCache

from core.events._base import Event


class EventDedup:
    def __init__(self, ttl: int = 30, maxsize: int = 2048):
        self._caches = [TTLCache(maxsize=maxsize // 4, ttl=ttl) for _ in range(4)]
        self._locks = [asyncio.Lock() for _ in range(4)]

    def _get_shard(self, key: str):
        shard_index = int(hashlib.sha256(key.encode()).hexdigest(), 16) % len(
            self._caches
        )
        return self._caches[shard_index], self._locks[shard_index]

    async def acquire(self, event: Event) -> bool:
        key = event.meta.key
        shard, lock = self._get_shard(key)

        async with lock:
            if key in shard:
                return False

            shard[key] = True

            return True

    async def release(self, event: Event) -> None:
        key = event.meta.key
        shard, lock = self._get_shard(key)

        async with lock:
            shard.pop(key, None)
