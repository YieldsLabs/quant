import asyncio
from dataclasses import dataclass, field
from typing import Generic, TypeVar, Union

from core.events._base import Event
from core.events.meta import EventMeta
from core.result import Result

T = TypeVar("T")


@dataclass(frozen=True)
class Query(Generic[T], Event):
    _response_event: asyncio.Event = field(default_factory=asyncio.Event, init=False)
    _response: Result[Union[T, None], Union[Exception, None]] = field(
        default=None, init=False
    )
    meta: EventMeta = field(default_factory=lambda: EventMeta(priority=1), init=False)

    def set_response(self, response: Result):
        object.__setattr__(self, "_response", response)
        self._response_event.set()

    async def wait_for_response(self) -> Result:
        await self._response_event.wait()
        return self._response
