import heapq
from asyncio import sleep
from dataclasses import dataclass, field
from typing import Dict, List

from .ohlcv import OHLCV


@dataclass()
class Timeseries:
    heap: List[OHLCV] = field(default_factory=list)
    timestamp_index: Dict[float, int] = field(default_factory=dict)
    capacity: int = 120000

    def add(self, bar: OHLCV):
        timestamp = bar.timestamp

        if timestamp in self.timestamp_index:
            index = self.timestamp_index[timestamp]
            self.heap[index] = bar
            self._sift_up(index)
        else:
            length = len(self.heap)

            if length >= self.capacity:
                oldest_bar = heapq.heappop(self.heap)
                self.timestamp_index.pop(oldest_bar.timestamp, None)

            self.heap.append(bar)
            self._sift_up(length - 1)
            self.timestamp_index[timestamp] = length - 1

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
        timestamp = curr_bar.timestamp
        index = self.timestamp_index.get(timestamp, None)

        if index is not None:
            for bar in self.heap[index + 1 :]:
                yield bar
                await sleep(0.001)

    def _sift_up(self, index: int):
        while index > 0:
            parent_index = (index - 1) // 2

            if self.heap[index] < self.heap[parent_index]:
                self.heap[index], self.heap[parent_index] = (
                    self.heap[parent_index],
                    self.heap[index],
                )
                self.timestamp_index[self.heap[index].timestamp] = index
                self.timestamp_index[self.heap[parent_index].timestamp] = parent_index
                index = parent_index
            else:
                break
