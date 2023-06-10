import asyncio
import os
from typing import Callable, Type

from .worker_pool import WorkerPool
from .event_handler import EventHandler
from .events.base_event import Event, EventEnded


class SingletonMeta(type):
    _instance = None

    def __call__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__call__(*args, **kwargs)
        return cls._instance


class EventDispatcher(metaclass=SingletonMeta):
    def __init__(self, num_workers: int = os.cpu_count() + 1, num_priority_group: int = 5):
        self.event_handler = EventHandler()
        self.cancel_event = asyncio.Event()
        self.worker_pool = WorkerPool(num_priority_group, num_workers, self.event_handler, self.cancel_event)

    def register(self, event_class: Type[Event], handler: Callable) -> None:
        self.event_handler.register(event_class, handler)

    def unregister(self, event_class: Type[Event], handler: Callable) -> None:
        self.event_handler.unregister(event_class, handler)

    async def dispatch(self, event: Event, *args, **kwargs) -> None:
        if isinstance(event, EventEnded):
            self.cancel_event.set()
        else:
            await self.worker_pool.dispatch_to_worker(event, *args, **kwargs)

    async def wait(self) -> None:
        await self.worker_pool.wait()

    async def stop(self) -> None:
        await self.dispatch(EventEnded())
