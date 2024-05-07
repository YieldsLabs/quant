import asyncio
import heapq
from bisect import bisect_right
from dataclasses import dataclass, field
from typing import List

from .ohlcv import OHLCV


@dataclass()
class Timeseries:
    heap: List["OHLCV"] = field(default_factory=list)
    capacity: int = 60000

    def enqueue(self, bar: OHLCV):
        if self.size >= self.capacity:
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

    async def find_next_bar(self, curr_bar: OHLCV, k=3):
        nearest = []
        index = bisect_right(self.heap, curr_bar)

        for i in range(index, len(self.heap)):
            next_bar = self.heap[i]
            heapq.heappush(
                nearest, (abs(next_bar.timestamp - curr_bar.timestamp), next_bar)
            )

            if len(nearest) > k:
                heapq.heappop(nearest)

        nearest_bars = [bar for _, bar in sorted(nearest, key=lambda x: x[0])]

        for bar in nearest_bars:
            yield bar

        await asyncio.sleep(0.001)
