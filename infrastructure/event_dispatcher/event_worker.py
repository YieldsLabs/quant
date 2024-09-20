import asyncio
from typing import Any, AsyncIterable, Dict, Tuple

from core.events.base import Event

from .event_handler import EventHandler


class EventWorker:
    def __init__(
        self,
        event_handler: EventHandler,
        cancel_event: asyncio.Event,
    ):
        self._event_handler = event_handler
        self._cancel_event = cancel_event
        self._queue = asyncio.Queue()

    @property
    def queue_size(self):
        return self._queue.qsize()

    async def run(self):
        async for event, args, kwargs in self._get_event_stream():
            await self._event_handler.handle_event(event, *args, **kwargs)

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
