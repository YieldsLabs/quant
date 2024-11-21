from contextlib import asynccontextmanager
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
        async with self._reader():
            return self._data.get(key, fallback)

    async def set(self, key: K, value: V) -> None:
        async with self._writer():
            old_value = self._data.get(key)
            self._data[key] = value
            self.on_set.emit(key=key, old_value=old_value, new_value=value)

    async def delete(self, key: K) -> bool:
        async with self._writer():
            old_value = self._data.pop(key, None)

            if old_value is not None:
                self.on_delete.emit(key=key, old_value=old_value)

            return old_value is not None

    async def reset(self):
        async with self._writer():
            cleared_data = dict(self._data)
            self._data.clear()
            self.on_reset.emit(cleared_data=cleared_data)

    async def exists(self, key: K) -> bool:
        async with self._reader():
            return key in self._data

    async def size(self) -> int:
        async with self._reader():
            return len(self._data)

    @asynccontextmanager
    async def _reader(self):
        await self._lock.acquire_reader()
        try:
            yield
        finally:
            await self._lock.release_reader()

    @asynccontextmanager
    async def _writer(self):
        await self._lock.acquire_writer()
        try:
            yield
        finally:
            await self._lock.release_writer()
