import asyncio
from functools import partial, wraps
import inspect
from typing import Callable, Type

from infrastructure.event_dispatcher.event_dispatcher import EventDispatcher

from .events.base_event import Event


def eda(cls: Type):
    class Wrapped(cls):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)

            self.dispatcher = EventDispatcher()

            self._registered_handlers = []

            for _, handler in inspect.getmembers(self.__class__, predicate=inspect.isfunction):
                if hasattr(handler, "event"):
                    event_type = handler.event
                    wrapped_handler = partial(handler, self)
                    self.dispatcher.register(event_type, wrapped_handler)

                    self._registered_handlers.append((event_type, wrapped_handler))

        def _unregister(self):
            for event_type, handler in self._registered_handlers:
                self.dispatcher.unregister(event_type, handler)

        def __del__(self):
            self._unregister()

        def __enter__(self):
            return self

        def __exit__(self, exc_type, exc_val, exc_tb):
            self._unregister()

    Wrapped.__name__ = cls.__name__
    Wrapped.__qualname__ = cls.__qualname__
    Wrapped.__doc__ = cls.__doc__
    Wrapped.__annotations__ = cls.__annotations__
    Wrapped.__module__ = cls.__module__

    return Wrapped


def register_handler(event_type: Type[Event]) -> Callable[[Callable], Callable]:
    def decorator(handler: Callable) -> Callable:
        if asyncio.iscoroutinefunction(handler):
            async def async_wrapped_handler(self, event: Event):
                return await handler(self, event)
        else:
            def async_wrapped_handler(self, event: Event):
                return handler(self, event)

        async_wrapped_handler.event = event_type
        async_wrapped_handler = wraps(handler)(async_wrapped_handler)

        return async_wrapped_handler

    return decorator
