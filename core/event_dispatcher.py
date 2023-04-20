import asyncio
from dataclasses import dataclass
from functools import partial, wraps
import inspect
from typing import Callable, Deque, Dict, List, Tuple, Type


@dataclass(frozen=True)
class Event:
    pass

class EventDispatcher:
    __instance: 'EventDispatcher' = None

    def __new__(cls) -> 'EventDispatcher':
        if not cls.__instance:
            cls.__instance = super().__new__(cls)
            cls.__instance.event_handlers: Dict[Type[Event], List[Callable]] = {}
            cls.__instance.event_queue = asyncio.Queue(maxsize=0)
            cls.__instance.cancel_event = asyncio.Event()
            cls.__instance.lock: asyncio.Lock = asyncio.Lock()
            cls.__instance.dead_letter_queue: List[Tuple[Event, Exception]] = []

        return cls.__instance

    def __init__(self):
        if not hasattr(self, "_process_events_task"):
            self._process_events_task = asyncio.create_task(self.process_events())

    def register(self, event_class: Type[Event], handler: Callable) -> None:
        if event_class not in self.event_handlers:
            self.event_handlers[event_class] = []

        self.event_handlers[event_class].append(handler)

    def unregister(self, event_class: Type[Event], handler: Callable) -> None:
        if event_class in self.event_handlers:
            self.event_handlers[event_class].remove(handler)

    async def dispatch(self, event: Event, *args, **kwargs) -> None:
        await self.event_queue.put((event, args, kwargs))

    async def process_events(self):
        while not self.cancel_event.is_set():
            event, args, kwargs = await self.event_queue.get()
            event_class = type(event)

            handlers = self.event_handlers.get(event_class, [])
            tasks = [self._call_handler(handler, event, *args, **kwargs) for handler in handlers]

            if tasks:
                await asyncio.gather(*tasks)

            self.event_queue.task_done()
            
            await asyncio.sleep(0.01)

    async def _call_handler(self, handler, event, *args, **kwargs):
        try:
            if asyncio.iscoroutinefunction(handler):
                await handler(event, *args, **kwargs)
            else:
                await asyncio.to_thread(handler, event, *args, **kwargs)
        except Exception as e:
            self.dead_letter_queue.append((event, e))

    async def wait(self) -> None:
        await self._process_events_task

    async def stop(self) -> None:
        self.cancel_event.set()
        await asyncio.shield(self._process_events_task)

def eda(cls: Type):
    class Wrapped(cls):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)

            self.dispatcher = EventDispatcher()

            for _, handler in inspect.getmembers(self.__class__, predicate=inspect.isfunction):
                if hasattr(handler, "event"):
                    event_type = handler.event

                    wrapped_handler = partial(handler, self)

                    self.dispatcher.register(event_type, wrapped_handler)

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