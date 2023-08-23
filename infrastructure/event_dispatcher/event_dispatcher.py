import asyncio
import os
from typing import Callable, Type

from core.events.base_event import Event, EventEnded

from .worker_pool import WorkerPool
from .event_handler import EventHandler


class SingletonMeta(type):
    _instance = None

    def __call__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__call__(*args, **kwargs)
        return cls._instance


class EventDispatcher(metaclass=SingletonMeta):
    def __init__(self, num_workers: int = os.cpu_count(), priority_multiplier: int = 2):
        self.event_handler = EventHandler()
        self.cancel_event = asyncio.Event()
        self.worker_pool = WorkerPool(num_workers, num_workers * priority_multiplier, self.event_handler, self.cancel_event)

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
       await asyncio.shield(self.worker_pool.wait())

    async def stop(self) -> None:
        await self.dispatch(EventEnded())
