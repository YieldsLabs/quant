import asyncio
import os
from typing import Callable, Type

from .worker_pool import WorkerPool
from .event_handler import EventHandler
from .events.base_event import EventEnded, Event


class SingletonMeta(type):
    _instance = None

    def __call__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__call__(*args, **kwargs)
        return cls._instance


class EventDispatcher(metaclass=SingletonMeta):
    def __init__(self, num_workers: int = os.cpu_count() + 1, num_priority_group: int = 5):
        self.cancel_event = asyncio.Event()
        self.event_handler = EventHandler()
        self.worker_pool = WorkerPool(num_priority_group, num_workers, self.event_handler, self.cancel_event)

    def register(self, event_class: Type[Event], handler: Callable) -> None:
        self.event_handler.register(event_class, handler)

    def unregister(self, event_class: Type[Event], handler: Callable) -> None:
        self.event_handler.unregister(event_class, handler)

    async def dispatch(self, event: Event, *args, **kwargs) -> None:
        await self.worker_pool.dispatch_to_worker(event.meta.priority, event, *args, **kwargs)

    async def wait(self) -> None:
        for worker in self.worker_pool.workers:
            await worker.queue.join()

    async def stop(self) -> None:
        self.cancel_event.set()
        await asyncio.sleep(0.1)

        while not all(worker.queue.empty() for worker in self.worker_pool.workers):
            await asyncio.sleep(0.1)

        for worker in self.worker_pool.workers:
            await worker.queue.put((EventEnded(), (), {}))

        await asyncio.shield(asyncio.gather(*(worker.task for worker in self.worker_pool.workers)))
