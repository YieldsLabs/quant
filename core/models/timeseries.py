from collections import deque
from dataclasses import dataclass, field
from typing import Deque

from .ohlcv import OHLCV


@dataclass()
class Timeseries:
    heap: Deque[OHLCV] = field(default_factory=lambda: deque(maxlen=600))
    bar_index: int = 0

    def enqueue(self, bar: OHLCV):
        self.heap.append(bar)
        self.heap = deque(sorted(self.heap, key=lambda x: x.timestamp), maxlen=600)
        self.bar_index += 1

    def dequeue(self):
        if self.is_empty:
            return None

        return self.heap.popleft()

    @property
    def is_empty(self):
        return not self.heap

    @property
    def size(self):
        return len(self.heap)

    @property
    def last(self):
        return self.heap[-1] if self.heap else None

    def find_next_bar(self, timestamp: int):
        left, right = 0, len(self.heap) - 1

        while left <= right:
            mid = (left + right) // 2
            if self.heap[mid].timestamp <= timestamp:
                left = mid + 1
            else:
                right = mid - 1

        for i in range(left, len(self.heap)):
            yield self.heap[i]

        yield None
