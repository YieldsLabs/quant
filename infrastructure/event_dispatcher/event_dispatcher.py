import asyncio
from typing import Callable, Optional, Type, Union

from core.commands._base import Command
from core.events._base import Event, EventEnded
from core.interfaces.abstract_config import AbstractConfig
from core.queries._base import Query
from core.result import Result
from core.tasks._base import Task
from infrastructure.event_store import EventStore

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
        self.config = config_service.get("bus")

        self._event_handler = EventHandler(self.config.get("timeout", 10))
        self._cancel_event = asyncio.Event()
        self._store = EventStore(config_service)

        self._command_worker_pool = None
        self._query_worker_pool = None
        self._event_worker_pool = None
        self._task_worker_pool = None

    @property
    def command_worker_pool(self):
        return self._get_worker_pool("_command_worker_pool")

    @property
    def query_worker_pool(self):
        return self._get_worker_pool("_query_worker_pool")

    @property
    def event_worker_pool(self):
        return self._get_worker_pool("_event_worker_pool")

    @property
    def task_worker_pool(self):
        return self._get_worker_pool("_task_worker_pool")

    def register(
        self,
        event_class: Type[Event],
        handler: Callable,
        filter_func: Optional[Callable[[Event], bool]] = None,
    ) -> None:
        self._event_handler.register(event_class, handler, filter_func)

    def unregister(self, event_class: Type[Event], handler: Callable) -> None:
        self._event_handler.unregister(event_class, handler)

    async def execute(self, command: Command, *args, **kwargs) -> Result:
        await self._dispatch_to_poll(command, self.command_worker_pool, *args, **kwargs)
        return await command.wait_for_execution()

    async def query(self, query: Query, *args, **kwargs) -> Result:
        await self._dispatch_to_poll(query, self.query_worker_pool, *args, **kwargs)
        return await query.wait_for_response()

    async def run(self, task: Task, *args, **kwargs) -> None:
        await self._dispatch_to_poll(task, self.task_worker_pool, *args, **kwargs)
        await task.wait_for_finishing()

    async def dispatch(self, event: Event, *args, **kwargs) -> None:
        await self._dispatch_to_poll(event, self.event_worker_pool, *args, **kwargs)
        self._store.append(event)

    async def wait(self) -> None:
        await asyncio.gather(
            *[
                self.event_worker_pool.wait(),
                self.query_worker_pool.wait(),
                self.command_worker_pool.wait(),
                self.task_worker_pool.wait(),
            ]
        )

    async def stop(self) -> None:
        await asyncio.gather(
            *[
                self._dispatch_to_poll(EventEnded(), self.event_worker_pool),
                self._dispatch_to_poll(EventEnded(), self.query_worker_pool),
                self._dispatch_to_poll(EventEnded(), self.command_worker_pool),
                self._dispatch_to_poll(EventEnded(), self.task_worker_pool),
            ]
        )
        self._store.close()

    async def _dispatch_to_poll(
        self,
        event: Union[Event, Command, Query],
        worker_pool: WorkerPool,
        *args,
        **kwargs,
    ) -> None:
        if isinstance(event, EventEnded):
            self._cancel_event.set()
        elif isinstance(event, (Command, Query, Event, Task)):
            await worker_pool.dispatch_to_worker(event, *args, **kwargs)
        else:
            raise ValueError(f"Invalid event type: {type(event)}")

    def _create_worker_pool(self) -> WorkerPool:
        return WorkerPool(
            self.config["num_workers"],
            self.config["piority_groups"],
            self._event_handler,
            self._cancel_event,
        )

    def _get_worker_pool(self, pool_attr: str) -> WorkerPool:
        if getattr(self, pool_attr) is None:
            setattr(self, pool_attr, self._create_worker_pool())

        return getattr(self, pool_attr)
