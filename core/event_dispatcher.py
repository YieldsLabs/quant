import asyncio
import inspect
from typing import Callable, Dict, List, Type


class Event:
    pass

class EventDispatcher:
    __instance = None
    
    def __new__(cls):
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)
            cls.__instance.event_handlers: Dict[Type[Event], List[Callable]] = {}
            cls.__instance.event_queue = asyncio.Queue()
            cls.__instance.lock = asyncio.Lock()
            cls.__instance.cancel_event = asyncio.Event()
        
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
            try:
                self.event_handlers[event_class].remove(handler)
            except ValueError:
                pass

    async def dispatch(self, event: Event, *args, **kwargs) -> None:
        await self.event_queue.put((event, args, kwargs))

    async def process_events(self):
        while not self.cancel_event.is_set():
            event, args, kwargs = await self.event_queue.get()

            async with self.lock:
                event_class = type(event)

                handlers = self.event_handlers.get(event_class, [])

            tasks = [self._call_handler(handler, event, *args, **kwargs) for handler in handlers]
            
            if not tasks:
                print(f"No handlers for event: {event_class}")
            else:
                await asyncio.gather(*tasks)

    async def _call_handler(self, handler, event, *args, **kwargs):
        try:
            if asyncio.iscoroutinefunction(handler):
                await handler(event, *args, **kwargs)
            else:
                await asyncio.to_thread(handler, event, *args, **kwargs)
        except Exception as e:
            print(f"Error in event handler: {e}")

    async def stop(self):
        self.cancel_event.set()
        await self._process_events_task

def eda(cls: Type):
    class Wrapped(cls):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.dispatcher = EventDispatcher()
            self.registered_handlers = []

            for _, method in inspect.getmembers(self.__class__, predicate=inspect.isfunction):
                if hasattr(method, "event"):
                    method(instance=self)
                    self.registered_handlers.append((method.event, method))
        
        def __del__(self):
            for event_class, handler in self.registered_handlers:
                self.dispatcher.unregister(event_class, handler)
    
    Wrapped.__name__ = cls.__name__
    Wrapped.__doc__ = cls.__doc__
    return Wrapped

def register_handler(event: Type[Event]):
    def decorator(handler: Callable):
        def wrapper(instance):
            instance.dispatcher.register(event, handler.__get__(instance, instance.__class__))
        wrapper.event = event
        return wrapper
    return decorator