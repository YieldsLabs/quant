import asyncio
from collections import defaultdict, deque
from functools import partial
import logging
from typing import Any, Callable, Deque, Dict, List, Optional, Tuple, Type, Union

from core.events.base import Event

HandlerType = Union[partial, Callable[..., Any]]


logger = logging.getLogger(__name__)


class EventHandler:
    def __init__(self):
        self._event_handlers: Dict[Type[Event], List[HandlerType]] = defaultdict(list)
        self._dead_letter_queue: Deque[Tuple[Event, Exception]] = deque(maxlen=100)

    @property
    def dlq(self):
        return self._dead_letter_queue

    def register(self, event_class: Type[Event], handler: HandlerType, filter_func: Optional[Callable[[Event], bool]] = None) -> None:
        self._event_handlers[event_class].append((handler, filter_func))

    def unregister(self, event_class: Type[Event], handler: HandlerType) -> None:
        try:
            self._event_handlers[event_class] = [
                (h, filter_fn)
                for h, filter_fn in self._event_handlers.get(event_class, [])
                if h != handler
            ]
        except ValueError:
            pass

    async def handle_event(self, event: Event, *args, **kwargs) -> None:
        event_type = type(event)
        handlers = self._event_handlers.get(event_type, [])

        for handler, filter_fn in handlers:
            if not filter_fn or filter_fn(event):
                await self._call_handler(handler, event, *args, **kwargs)

    async def _call_handler(self, handler: HandlerType, event: Event, *args, **kwargs) -> None:
        try:
            await self._create_handler(handler, event, *args, **kwargs)
            logger.debug(event, handler)
        except Exception as e:
            self._dead_letter_queue.append((event, e))
            logger.error(f"Exception encountered: {e}. Event added to dead letter queue.")

    async def _create_handler(self, handler: HandlerType, event: Event, *args, **kwargs) -> None:
        if asyncio.iscoroutinefunction(handler):
            await handler(event, *args, **kwargs)
        else:
            await asyncio.to_thread(handler, event, *args, **kwargs)
