import asyncio
from collections import deque
from typing import Any, AsyncIterable, Dict, Tuple

import numpy as np

from core.events._base import Event

from .event_handler import EventHandler


class EventWorker:
    def __init__(
        self,
        event_handler: EventHandler,
        cancel_event: asyncio.Event,
        task_duration_limit: int = 100,
    ):
        self._event_handler = event_handler
        self._cancel_event = cancel_event
        self._queue = asyncio.Queue()
        self._task_durations = deque(maxlen=task_duration_limit)

    @property
    def score(self):
        return self._queue.qsize(), (
            np.mean(self._task_durations) if len(self._task_durations) > 2 else 0.0
        )

    async def run(self):
        async for event, args, kwargs in self._get_event_stream():
            start_time = asyncio.get_event_loop().time()

            await self._event_handler.handle_event(event, *args, **kwargs)

            end_time = asyncio.get_event_loop().time()
            self._task_durations.append(end_time - start_time)

    async def _get_event_stream(
        self,
    ) -> AsyncIterable[Tuple[Event, Tuple[Any], Dict[str, Any]]]:
        while not self._cancel_event.is_set():
            event, args, kwargs = await self._queue.get()

            yield event, args, kwargs

            self._queue.task_done()

    async def dispatch(self, event: Event, *args, **kwargs) -> None:
        await self._queue.put((event, args, kwargs))

    async def wait(self) -> None:
        await self._queue.join()
