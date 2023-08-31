import asyncio
from functools import partial, wraps
import inspect
from typing import Callable, Type

from infrastructure.event_dispatcher.event_dispatcher import EventDispatcher

from .events.base import Event
from .commands.base import Command
from .queries.base import Query


def eda(cls: Type):
    class Wrapped(cls):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)

            self._dispatcher = EventDispatcher()

            self._registered_handlers = []

            for _, handler in inspect.getmembers(self.__class__, predicate=inspect.isfunction):
                if hasattr(handler, "event"):
                    event_type = handler.event
                    wrapped_handler = partial(handler, self)
                    self._dispatcher.register(event_type, wrapped_handler)

                    self._registered_handlers.append((event_type, wrapped_handler))
        
        async def dispatch(self, event, *args, **kwargs):
            await self._dispatcher.dispatch(event, *args, **kwargs)

        async def query(self, query, *args, **kwargs):
            return await self._dispatcher.query(query, *args, **kwargs)
        
        async def execute(self, command, *args, **kwargs):
            return await self._dispatcher.execute(command, *args, **kwargs)

        def _unregister(self):
            for event_type, handler in self._registered_handlers:
                self._dispatcher.unregister(event_type, handler)
            self._registered_handlers = []

        def __del__(self):
            self._unregister()

        async def __aenter__(self):
            return self

        async def __aexit__(self, exc_type, exc_val, exc_tb):
            await self._dispatcher.wait()
            self._unregister()

    Wrapped.__name__ = cls.__name__
    Wrapped.__qualname__ = cls.__qualname__
    Wrapped.__doc__ = cls.__doc__
    Wrapped.__annotations__ = cls.__annotations__
    Wrapped.__module__ = cls.__module__

    return Wrapped


def event_handler(event_type: Type[Event]) -> Callable[[Callable], Callable]:
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

def command_handler(command_type: Type[Command]) -> Callable[[Callable], Callable]:
    def decorator(handler: Callable) -> Callable:
        if asyncio.iscoroutinefunction(handler):
            async def async_wrapped_handler(self, command: Command):
                await handler(self, command)
                command.executed()
                return
        else:
            def async_wrapped_handler(self, command: Command):
                handler(self, command)
                command.executed()

        async_wrapped_handler.event = command_type
        async_wrapped_handler = wraps(handler)(async_wrapped_handler)

        return async_wrapped_handler

    return decorator

def query_handler(query_type: Type[Query]) -> Callable[[Callable], Callable]:
    def decorator(handler: Callable) -> Callable:
        if asyncio.iscoroutinefunction(handler):
            async def async_wrapped_handler(self, query: Query):
                response = await handler(self, query)
                query.set_response(response)
                return
        else:
            def async_wrapped_handler(self, query: Query):
                response = handler(self, query)
                query.set_response(response)
                return

        async_wrapped_handler.event = query_type
        async_wrapped_handler = wraps(handler)(async_wrapped_handler)

        return async_wrapped_handler

    return decorator
