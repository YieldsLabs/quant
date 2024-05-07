import asyncio
from collections import deque
from dataclasses import dataclass, field
from typing import Deque

from .ohlcv import OHLCV


@dataclass()
class Timeseries:
    heap: Deque[OHLCV] = field(default_factory=lambda: deque(maxlen=377))

    def enqueue(self, bar: OHLCV):
        self.heap.append(bar)
        self.heap = deque(sorted(self.heap, key=lambda x: x.timestamp), maxlen=377)

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
            return float('inf')
        
        diff_sum = 0
        
        for i in range(1, len(self.heap)):
            diff_sum += self.heap[i].timestamp - self.heap[i - 1].timestamp
        
        return diff_sum / (len(self.heap) - 1)

    async def find_next_bar(self, timestamp: int):
        left, right = 0, len(self.heap) - 1

        while left <= right:
            mid = (left + right) // 2
            
            if self.heap[mid].timestamp <= timestamp:
                left = mid + 1
            else:
                right = mid - 1

        avg_time_diff = self.avg_time_diff()

        for i in range(left, len(self.heap)):
            next_bar = self.heap[i]
            
            if next_bar.timestamp - timestamp <= avg_time_diff:
                await asyncio.sleep(0.001)
                yield next_bar
                
        yield None
