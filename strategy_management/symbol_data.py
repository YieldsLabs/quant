import asyncio
from collections import deque


class SymbolData:
    def __init__(self, size: int):
        self.buffer = deque(maxlen=size)
        self.lock = asyncio.Lock()

    @property
    def count(self):
        return len(self.buffer)

    async def append(self, event):
        async with self.lock:
            self.buffer.append(event)

    async def get_window(self):
        async with self.lock:
            return list(self.buffer)
