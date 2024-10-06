import asyncio
from typing import Any, AsyncIterable, Awaitable, Callable, Optional

from core.events._base import Event


class DataCollector:
    def __init__(self):
        self.queue = asyncio.Queue()
        self.producers = []
        self.consumers = []
        self.tasks = set()

    async def start(self, msg: Event):
        for producer in self.producers:
            task = asyncio.create_task(self._run_producer(producer, msg))
            self.tasks.add(task)
            task.add_done_callback(self.tasks.discard)

        for consumer in self.consumers:
            task = asyncio.create_task(self._run_consumer(consumer))
            self.tasks.add(task)

            task.add_done_callback(self.tasks.discard)

    async def stop(self):
        await self.queue.put(None)
        await self.queue.join()
        await self.wait_for_completion()
        self.tasks.clear()

    async def wait_for_completion(self):
        await asyncio.gather(*self.tasks, return_exceptions=True)

    def add_producer(self, producer: Callable[[Optional[Event]], AsyncIterable[Any]]):
        self.producers.append(producer)

    def add_consumer(self, consumer: Callable[[Any], Awaitable[None]]):
        self.consumers.append(consumer)

    async def _run_producer(self, producer, msg):
        async for data in producer(msg):
            await self.queue.put(data)

        await self.queue.put(None)

    async def _run_consumer(self, consumer):
        while True:
            data = await self.queue.get()
            if data is None:
                break

            await consumer(data)

            self.queue.task_done()
