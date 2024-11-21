from typing import Any, Callable, List


class Signal:
    def __init__(self):
        self._subscribers: List[Callable[..., Any]] = []

    def connect(self, subscriber: Callable[..., Any]) -> None:
        self._subscribers.append(subscriber)

    def emit(self, *args, **kwargs) -> None:
        for subscriber in self._subscribers:
            subscriber(*args, **kwargs)
