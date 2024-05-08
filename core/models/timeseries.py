import heapq
from asyncio import sleep
from bisect import bisect_right
from dataclasses import dataclass, field
from typing import List

from .ohlcv import OHLCV


@dataclass()
class Timeseries:
    heap: List[OHLCV] = field(default_factory=list)
    capacity: int = 120000

    def enqueue(self, bar: OHLCV):
        heapq.heappush(self.heap, bar)

        if len(self.heap) > self.capacity:
            heapq.heappop(self.heap)

    @property
    def is_empty(self):
        return not self.heap

    @property
    def size(self):
        return len(self.heap)

    @property
    def last(self):
        return self.heap[-1] if not self.is_empty else None

    async def find_next_bar(self, curr_bar: OHLCV):
        index = bisect_right(self.heap, curr_bar)

        for bar in self.heap[index:]:
            yield bar
            await sleep(0.001)
