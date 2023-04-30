import asyncio
from collections import deque
from functools import partial, wraps
import inspect
import os
import random
from typing import Any, AsyncIterable, Callable, Deque, Dict, List, Tuple, Type

import numpy as np

from .events.base_event import EndEvent, Event


class EventDispatcher:
    __instance: 'EventDispatcher' = None

    def __new__(cls) -> 'EventDispatcher':
        if not cls.__instance:
            cls.__instance = super().__new__(cls)
            cls.__instance.event_handlers: Dict[Type[Event], List[Callable]] = {}
            cls.__instance.cancel_event = asyncio.Event()
            cls.__instance.all_workers_done = asyncio.Event()
            cls.__instance.dead_letter_queue: Deque[Tuple[Event, Exception]] = deque(maxlen=100)

        return cls.__instance

    def __init__(self, num_workers: int = os.cpu_count() + 1, priority_groups: int = 5):
        if not hasattr(self, "_worker_tasks"):
            self._initialize_worker_tasks(num_workers, priority_groups)
            self._initialize_load_balancer(priority_groups)

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

            if not handlers:
                continue

            tasks = [self._call_handler(handler, event, *args, **kwargs) for handler in handlers]

            await asyncio.gather(*tasks)

        self.all_workers_done.set()

    async def wait(self) -> None:
        await self.all_workers_done.wait()
        self.all_workers_done.clear()

    async def stop(self) -> None:
        self.cancel_event.set()
        await self.stop_workers()
        await asyncio.shield(asyncio.gather(*self._worker_tasks))

    async def stop_workers(self) -> None:
        await asyncio.sleep(0.1)

        while not all(queue.empty() for queue in self._group_event_queues):
            await asyncio.sleep(0.1)

        for _ in range(len(self._worker_tasks)):
            await self.dispatch(EndEvent())

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

            if isinstance(event, EndEvent):
                break

            yield event, args, kwargs

            self._group_event_queues[priority_group].task_done()

    def _determine_priority_group(self, priority: int) -> int:
        total_events = self._group_event_counts.sum()

        if total_events == 0:
            return min(priority, len(self._group_event_queues) - 1)

        processed_ratios = self._group_event_counts / total_events

        errors = self._target_ratios - processed_ratios

        self._integral_errors += errors

        derivative_errors = errors - self._previous_errors

        self._previous_errors = errors

        control_outputs = (
            self._kp * errors + self._ki * self._integral_errors + self._kd * derivative_errors
        )

        control_output_sum = control_outputs.sum()

        weights = control_outputs / control_output_sum

        return random.choices(range(len(control_outputs)), weights=weights)[0]

    def _initialize_worker_tasks(self, num_workers: int, priority_groups: int):
        self._worker_tasks = []
        self._group_event_queues = [asyncio.Queue() for _ in range(priority_groups)]
        self._group_event_counts = np.zeros(priority_groups)

        workers_per_group = num_workers // priority_groups
        remaining_workers = num_workers % priority_groups

        for priority_group in range(priority_groups):
            num_workers_for_group = workers_per_group + (1 if remaining_workers > 0 else 0)
            remaining_workers -= 1
            tasks = [asyncio.create_task(self.process_events(priority_group)) for _ in range(num_workers_for_group)]
            self._worker_tasks.extend(tasks)

    def _initialize_load_balancer(self, priority_groups: int):
        self._kp = 1.0
        self._ki = 0.6
        self._kd = 0.3

        self._integral_errors = np.zeros(priority_groups)
        self._previous_errors = np.zeros(priority_groups)
        self._target_ratios = 1 / (np.arange(priority_groups) + 1)


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
