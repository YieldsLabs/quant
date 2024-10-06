import asyncio
from typing import Awaitable, Callable, Optional

from core.events._base import Event


class DataCollector:
    def __init__(self):
        self.queue = asyncio.Queue()
        self.producers = []
        self.consumers = []
        self.tasks = set()

    async def start(self, msg: Event):
        for producer in self.producers:
            task = asyncio.create_task(producer(self.queue, msg))
            self.tasks.add(task)
            task.add_done_callback(self.tasks.discard)

        for consumer in self.consumers:
            task = asyncio.create_task(consumer(self.queue))
            self.tasks.add(task)

            task.add_done_callback(self.tasks.discard)

    async def stop(self):
        await self.queue.put(None)
        await self.wait_for_completion()
        self.tasks.clear()

    async def wait_for_completion(self):
        await asyncio.gather(*self.tasks, return_exceptions=True)

    def add_producer(
        self, producer: Callable[[asyncio.Queue, Optional[Event]], Awaitable[None]]
    ):
        self.producers.append(producer)

    def add_consumer(self, consumer: Callable[[asyncio.Queue], Awaitable[None]]):
        self.consumers.append(consumer)
