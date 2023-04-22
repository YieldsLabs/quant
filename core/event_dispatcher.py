import asyncio
from functools import partial, wraps
import inspect
import os
import random
from typing import Any, AsyncIterable, Callable, Dict, List, Tuple, Type

from .events.base_event import Event

class EventDispatcher:
    __instance: 'EventDispatcher' = None
    __slots__ = ('event_handlers', 'cancel_event', 'dead_letter_queue', '_worker_tasks', '_group_event_queues', '_group_event_counts', '_group_priorities')

    def __new__(cls) -> 'EventDispatcher':
        if not cls.__instance:
            cls.__instance = super().__new__(cls)
            cls.__instance.event_handlers: Dict[Type[Event], List[Callable]] = {}
            cls.__instance.cancel_event = asyncio.Event()
            cls.__instance.dead_letter_queue: List[Tuple[Event, Exception]] = []

        return cls.__instance

    def __init__(self, num_workers: int = os.cpu_count(), priority_groups: int = 4):
        if not hasattr(self, "_worker_tasks"):
            self._worker_tasks = []
            self._group_event_queues = [asyncio.Queue() for _ in range(priority_groups)]
            self._group_event_counts = [0] * priority_groups
            self._group_priorities = list(range(priority_groups)) 

            for priority_group in range(priority_groups):
                tasks = [asyncio.create_task(self.process_events(priority_group)) for _ in range(num_workers)]
                
                self._worker_tasks.extend(tasks)

    def register(self, event_class: Type[Event], handler: Callable) -> None:
        self.event_handlers.setdefault(event_class, []).append(handler)

    def unregister(self, event_class: Type[Event], handler: Callable) -> None:
        if event_class in self.event_handlers:
            self.event_handlers[event_class].remove(handler)

    async def dispatch(self, event: Event, *args, **kwargs) -> None:
        priority_group = self._determine_priority_group(event.meta.priority)
        await self._group_event_queues[priority_group].put((event, args, kwargs))

    async def process_events(self, priority_group):
        async for event, args, kwargs in self._get_event_stream(priority_group):
            handlers = self.event_handlers.get(type(event), [])
            
            tasks = [self._call_handler(handler, event, *args, **kwargs) for handler in handlers]

            if not tasks:
                continue
            
            await asyncio.gather(*tasks)
    
    async def wait(self) -> None:
        await asyncio.gather(*self._worker_tasks)

    async def stop(self) -> None:
        self.cancel_event.set()
        await asyncio.shield(asyncio.gather(*self._worker_tasks))

    async def _call_handler(self, handler, event, *args, **kwargs):
        try:
            if asyncio.iscoroutinefunction(handler):
                await handler(event, *args, **kwargs)
            else:
                await asyncio.to_thread(handler, event, *args, **kwargs)
        except Exception as e:
            self.dead_letter_queue.append((event, e))
    
    async def _get_event_stream(self, priority_group) -> AsyncIterable[Tuple[Event, Tuple[Any], Dict[str, Any]]]:
        while not self.cancel_event.is_set():
            event, args, kwargs = await self._group_event_queues[priority_group].get()
            
            yield event, args, kwargs
            
            self._group_event_queues[priority_group].task_done()

    def _determine_priority_group(self, priority: int) -> int:
        total_events = sum(self._group_event_counts)

        if total_events == 0:
            return min(priority, len(self._group_event_queues) - 1)

        processed_ratios = [count / total_events for count in self._group_event_counts]
        target_ratios = [1 / p for p in self._group_priorities]
        total_target_ratio = sum(target_ratios)
        target_ratios = [tr / total_target_ratio for tr in target_ratios]

        errors = [target - processed for target, processed in zip(target_ratios, processed_ratios)]
        
        integral_action = 0.5

        control_outputs = [error + integral_action * sum(errors[: i + 1]) for i, error in enumerate(errors)]

        return random.choice([i for i, v in enumerate(control_outputs) if v == max(control_outputs)])

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