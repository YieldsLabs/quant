import asyncio
from dataclasses import dataclass, field
from enum import Enum
from typing import Generic, TypeVar

from core.events.base import Event, EventMeta

T = TypeVar("T")


class QueryGroup(Enum):
    account = "account"
    broker = "broker"
    position = "position"
    portfolio = "portfolio"

    def __str__(self):
        return self.value


@dataclass(frozen=True)
class Query(Generic[T], Event):
    _response_event: asyncio.Event = field(default_factory=asyncio.Event, init=False)
    _response: T = field(default=None, init=False)
    meta: EventMeta = field(default_factory=lambda: EventMeta(priority=1), init=False)

    def set_response(self, response: T):
        object.__setattr__(self, "_response", response)
        self._response_event.set()

    async def wait_for_response(self) -> T:
        await self._response_event.wait()
        return self._response
