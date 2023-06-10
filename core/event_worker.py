import asyncio
from typing import Any, AsyncIterable, Dict, Tuple

from .throughput_monitor import ThroughputMonitor
from .event_handler import EventHandler
from .events.base_event import Event


class EventWorker:
    def __init__(self, event_handler: EventHandler, cancel_event: asyncio.Event):
        self.event_handler = event_handler
        self.cancel_event = cancel_event
        self.queue = asyncio.Queue()
        self.task = asyncio.create_task(self._process_events())
        self.throughput_monitor = ThroughputMonitor()

    async def _process_events(self):
        async for event, args, kwargs in self._get_event_stream():
            await self.event_handler.handle_event(event, *args, **kwargs)

            self.throughput_monitor.event_processed()

    async def _get_event_stream(self) -> AsyncIterable[Tuple[Event, Tuple[Any], Dict[str, Any]]]:
        while not self.cancel_event.is_set():
            event, args, kwargs = await self.queue.get()

            yield event, args, kwargs

            self.queue.task_done()

    async def dispatch(self, event: Event, *args, **kwargs) -> None:
        await self.queue.put((event, args, kwargs))

    async def wait(self) -> None:
        await self.queue.join()
