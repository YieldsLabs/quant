import asyncio
from bisect import bisect_right
from dataclasses import dataclass, field
from typing import List

from .ohlcv import OHLCV


@dataclass()
class Timeseries:
    heap: List["OHLCV"] = field(default_factory=list)
    lock: asyncio.Lock = field(default_factory=asyncio.Lock)
    capacity: int = 560
    total_time_diff: int = 0.0

    async def enqueue(self, bar: OHLCV):
        async with self.lock:
            if self.last:
                self.total_time_diff += bar.timestamp - self.last.timestamp

            if self.size >= self.capacity:
                self.total_time_diff -= self.heap[0].timestamp - self.heap[1].timestamp
                self.heap.pop(0)

            index = bisect_right(self.heap, bar)
            self.heap.insert(index, bar)

    @property
    def is_empty(self):
        return not self.heap

    @property
    def size(self):
        return len(self.heap)

    @property
    def last(self):
        return self.heap[-1] if self.heap else None

    async def avg_time_diff(self):
        async with self.lock:
            if len(self.heap) <= 1:
                return float("inf")

            return self.total_time_diff / (len(self.heap) - 1)

    async def find_next_bar(self, timestamp: int):
        avg_time_diff = await self.avg_time_diff()

        left, right = 0, len(self.heap) - 1

        while left <= right:
            mid = (left + right) // 2

            if self.heap[mid].timestamp <= timestamp:
                left = mid + 1
            else:
                right = mid - 1

        for i in range(left, len(self.heap)):
            next_bar = self.heap[i]

            if next_bar.timestamp - timestamp <= avg_time_diff:
                await asyncio.sleep(0.001)
                yield next_bar

        yield None
