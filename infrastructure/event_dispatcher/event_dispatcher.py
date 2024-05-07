import asyncio
from typing import Any, Callable, Optional, Type

from core.commands.base import Command
from core.events.base import Event, EventEnded
from core.interfaces.abstract_config import AbstractConfig
from core.queries.base import Query
from infrastructure.event_store.event_store import EventStore

from .event_handler import EventHandler
from .worker_pool import WorkerPool


class SingletonMeta(type):
    _instance = None

    def __call__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__call__(*args, **kwargs)
        return cls._instance


class EventDispatcher(metaclass=SingletonMeta):
    def __init__(self, config_service: AbstractConfig):
        self.event_handler = EventHandler()
        self.cancel_event = asyncio.Event()

        self.config = config_service.get("bus")
        self._store = EventStore(config_service)

        self._command_worker_pool = None
        self._query_worker_pool = None
        self._event_worker_pool = None

    @property
    def command_worker_pool(self):
        if self._command_worker_pool is None:
            self._command_worker_pool = self._create_worker_pool()
        return self._command_worker_pool

    @property
    def query_worker_pool(self):
        if self._query_worker_pool is None:
            self._query_worker_pool = self._create_worker_pool()
        return self._query_worker_pool

    @property
    def event_worker_pool(self):
        if self._event_worker_pool is None:
            self._event_worker_pool = self._create_worker_pool()
        return self._event_worker_pool

    def register(
        self,
        event_class: Type[Event],
        handler: Callable,
        filter_func: Optional[Callable[[Event], bool]] = None,
    ) -> None:
        self.event_handler.register(event_class, handler, filter_func)

    def unregister(self, event_class: Type[Event], handler: Callable) -> None:
        self.event_handler.unregister(event_class, handler)

    async def execute(self, command: Command, *args, **kwargs) -> None:
        await self._dispatch_to_poll(command, self.command_worker_pool, *args, **kwargs)
        await command.wait_for_execution()

    async def query(self, query: Query, *args, **kwargs) -> Any:
        await self._dispatch_to_poll(query, self.query_worker_pool, *args, **kwargs)
        return await query.wait_for_response()

    async def dispatch(self, event: Event, *args, **kwargs) -> None:
        await self._dispatch_to_poll(event, self.event_worker_pool, *args, **kwargs)
        self._store.append(event)

    async def wait(self) -> None:
        await asyncio.gather(
            *[
                self.event_worker_pool.wait(),
                self.query_worker_pool.wait(),
                self.command_worker_pool.wait(),
            ]
        )

    async def stop(self) -> None:
        await asyncio.gather(
            *[
                self._dispatch_to_poll(EventEnded(), self.event_worker_pool),
                self._dispatch_to_poll(EventEnded(), self.query_worker_pool),
                self._dispatch_to_poll(EventEnded(), self.command_worker_pool),
            ]
        )
        self._store.close()

    async def _dispatch_to_poll(
        self, event: Type[Event], worker_pool: WorkerPool, *args, **kwargs
    ) -> None:
        if isinstance(event, EventEnded):
            self.cancel_event.set()
            return

        await worker_pool.dispatch_to_worker(event, *args, **kwargs)

    def _create_worker_pool(self) -> WorkerPool:
        return WorkerPool(
            self.config["num_workers"],
            self.config["piority_groups"],
            self.event_handler,
            self.cancel_event,
        )
