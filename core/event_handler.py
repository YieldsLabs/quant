import asyncio
from collections import deque
from functools import partial
from typing import Deque, Dict, List, Tuple, Type

from .events.base_event import Event


class EventHandler:
    def __init__(self):
        self.event_handlers: Dict[Type[Event], List[partial]] = {}
        self.dead_letter_queue: Deque[Tuple[Event, Exception]] = deque(maxlen=100)

    def register(self, event_class: Type[Event], handler: partial) -> None:
        self.event_handlers.setdefault(event_class, []).append(handler)

    def unregister(self, event_class: Type[Event], handler: partial) -> None:
        if event_class in self.event_handlers and handler in self.event_handlers[event_class]:
            self.event_handlers[event_class].remove(handler)

    async def handle_event(self, event: Event, *args, **kwargs) -> None:
        handlers = self.event_handlers.get(type(event), [])

        if not handlers:
            return

        tasks = [self._call_handler(handler, event, *args, **kwargs) for handler in handlers]
        await asyncio.gather(*tasks)

    async def _call_handler(self, handler, event, *args, **kwargs):
        try:
            if asyncio.iscoroutinefunction(handler):
                await handler(event, *args, **kwargs)
            else:
                await asyncio.to_thread(handler, event, *args, **kwargs)
        except Exception as e:
            print(e)
            self.dead_letter_queue.append((event, e))
