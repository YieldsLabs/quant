import asyncio
from dataclasses import dataclass, field

from core.events._base import Event
from core.events.meta import EventMeta


@dataclass(frozen=True)
class Task(Event):
    _task_event: asyncio.Event = field(default_factory=asyncio.Event, init=False)
    _task: asyncio.Task = field(default=None, init=False)
    meta: EventMeta = field(default_factory=lambda: EventMeta(priority=1), init=False)

    def set_task(self, task: asyncio.Task):
        object.__setattr__(self, "_task", task)
        self._task_event.set()

    async def wait_for_finishing(self) -> asyncio.Task:
        await self._task_event.wait()
        result = await self._task

        if not self._task.done():
            self._task.cancel()

        object.__setattr__(self, "_task", None)

        return result
