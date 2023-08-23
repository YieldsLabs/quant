import asyncio
from collections import deque
from functools import partial
from typing import Any, Callable, Deque, Dict, List, Tuple, Type, Union

from core.events.base_event import Event

HandlerType = Union[partial, Callable[..., Any]]


class EventHandler:
    def __init__(self):
        self._event_handlers: Dict[Type[Event], List[HandlerType]] = {}
        self._dead_letter_queue: Deque[Tuple[Event, Exception]] = deque(maxlen=100)

    @property
    def dlq(self):
        return self._dead_letter_queue

    def register(self, event_class: Type[Event], handler: HandlerType) -> None:
        if event_class in self._event_handlers:
            self._event_handlers[event_class].append(handler)
        else:
            self._event_handlers[event_class] = [handler]

    def unregister(self, event_class: Type[Event], handler: HandlerType) -> None:
        if event_class in self._event_handlers:
            try:
                self._event_handlers[event_class].remove(handler)
            except ValueError:
                pass

    async def handle_event(self, event: Event, *args, **kwargs) -> None:
        event_type = type(event)

        if event_type in self._event_handlers:
            await asyncio.gather(*[self._call_handler(handler, event, *args, **kwargs) for handler in self._event_handlers[event_type]])

    async def _call_handler(self, handler: HandlerType, event: Event, *args, **kwargs) -> None:
        try:
            await self._execute_handler(handler, event, *args, **kwargs)
        except Exception as e:
            print(e)
            self._dead_letter_queue.append((event, e))

    async def _execute_handler(self, handler: HandlerType, event: Event, *args, **kwargs) -> None:
        if asyncio.iscoroutinefunction(handler):
            await handler(event, *args, **kwargs)
        else:
            await asyncio.to_thread(handler, event, *args, **kwargs)
