import asyncio
from typing import Any, Callable, List


class Signal:
    def __init__(self):
        self._subscribers: List[Callable[..., Any]] = []

    def connect(self, subscriber: Callable[..., Any]) -> None:
        self._subscribers.append(subscriber)

    def emit(self, *args, **kwargs) -> None:
        tasks = []

        for subscriber in self._subscribers:
            if asyncio.iscoroutinefunction(subscriber):
                tasks.append(subscriber(*args, **kwargs))
            else:
                subscriber(*args, **kwargs)

        if tasks:
            asyncio.create_task(self._run_async_subscribers(tasks))

    @staticmethod
    async def _run_async_subscribers(tasks: List[asyncio.Future]) -> None:
        await asyncio.gather(*tasks)
