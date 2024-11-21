import asyncio
from dataclasses import dataclass, field
from typing import Dict, Generic, Optional, TypeVar

from ._rw import RWLock
from ._signal import Signal

K = TypeVar("K")
V = TypeVar("V")


@dataclass(repr=False, eq=False, slots=True)
class InMemory(Generic[K, V]):
    _data: Dict[K, V] = field(default_factory=dict)
    _lock: RWLock = field(default_factory=RWLock)

    on_set: Signal = field(default_factory=Signal)
    on_delete: Signal = field(default_factory=Signal)
    on_reset: Signal = field(default_factory=Signal)

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
