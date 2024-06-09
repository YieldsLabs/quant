import asyncio
import logging
from collections import defaultdict, deque
from functools import partial
from typing import Any, Callable, Deque, Dict, List, Optional, Tuple, Type, Union

from core.commands.base import Command
from core.events.base import Event
from core.queries.base import Query

HandlerType = Union[partial, Callable[..., Any]]


logger = logging.getLogger(__name__)


class EventHandler:
    def __init__(self):
        self._event_handlers: Dict[Type[Event], List[HandlerType]] = defaultdict(list)
        self._dlq: Deque[Tuple[Event, Exception]] = deque(maxlen=100)

    @property
    def dlq(self):
        return self._dlq

    def register(
        self,
        event_class: Type[Event],
        handler: HandlerType,
        filter_func: Optional[Callable[[Event], bool]] = None,
    ) -> None:
        self._event_handlers[event_class].append((handler, filter_func))

    def unregister(self, event_class: Type[Event], handler: HandlerType) -> None:
        self._event_handlers[event_class] = [
            (h, filter_fn)
            for h, filter_fn in self._event_handlers.get(event_class, [])
            if h != handler
        ]

    async def handle_event(self, event: Event, *args, **kwargs) -> None:
        handlers = self._event_handlers.get(type(event), [])

        for handler, filter_fn in handlers:
            if not filter_fn or filter_fn(event):
                try:
                    await self._call_handler(handler, event, *args, **kwargs)
                except Exception as e:
                    self._handle_exception(handler, event, e)

    async def _call_handler(
        self, handler: HandlerType, event: Event, *args, **kwargs
    ) -> None:
        if asyncio.iscoroutinefunction(handler):
            response = await handler(event, *args, **kwargs)
        else:
            response = await asyncio.to_thread(handler, event, *args, **kwargs)

        if isinstance(event, Query):
            event.set_response(response)
        elif isinstance(event, Command):
            event.executed()

    def _handle_exception(
        self, handler: HandlerType, event: Event, exception: Exception
    ) -> None:
        logger.error(
            f"Exception encountered in event {event}:{handler} {exception}. Event added to dead letter queue."
        )

        if isinstance(event, Command):
            event.executed()
        elif isinstance(event, Query):
            event.set_response(None)

        self._dlq.append((event, exception))
