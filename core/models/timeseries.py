import asyncio
from bisect import bisect_right
from dataclasses import dataclass, field
from typing import List

from .ohlcv import OHLCV


@dataclass()
class Timeseries:
    heap: List["OHLCV"] = field(default_factory=list)
    capacity: int = 1200
    total_time_diff: int = 0.0

    def enqueue(self, bar: OHLCV):
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

    def avg_time_diff(self):
        if len(self.heap) <= 1:
            return float("inf")

        return self.total_time_diff / (len(self.heap) - 1)

    async def find_next_bar(self, curr_bar: OHLCV):
        avg_time_diff = self.avg_time_diff()

        index = bisect_right(self.heap, curr_bar)
        for i in range(index, len(self.heap)):
            next_bar = self.heap[i]

            if next_bar.timestamp - curr_bar.timestamp <= avg_time_diff:
                await asyncio.sleep(0.001)
                yield next_bar

        yield None
