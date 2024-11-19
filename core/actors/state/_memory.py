import asyncio
from typing import Dict, Generic, Optional, TypeVar

from ._rw import RWLock

K = TypeVar("K")
V = TypeVar("V")


class InMemory(Generic[K, V]):
    def __init__(self):
        self._data: Dict[K, V] = {}
        self._lock = RWLock()

    async def get(self, key: K, fallback: Optional[V] = None) -> Optional[V]:
        await self._lock.acquire_reader()

        try:
            return self._data.get(key, fallback)
        except asyncio.CancelledError:
            raise
        finally:
            await self._lock.release_reader()

    async def set(self, key: K, value: V) -> None:
        await self._lock.acquire_writer()

        try:
            self._data[key] = value
        finally:
            await self._lock.release_writer()

    async def delete(self, key: K) -> bool:
        await self._lock.acquire_writer()

        try:
            return self._data.pop(key, None) is not None
        finally:
            await self._lock.release_writer()

    async def reset(self):
        await self._lock.acquire_writer()

        try:
            self._data.clear()
        finally:
            await self._lock.release_writer()

    async def exists(self, key: K) -> bool:
        return await self.get(key) is not None

    async def size(self) -> int:
        await self._lock.acquire_reader()

        try:
            return len(self._data)
        finally:
            await self._lock.release_reader()
