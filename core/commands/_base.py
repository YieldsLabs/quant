import asyncio
import hashlib
from dataclasses import dataclass, field, fields
from datetime import datetime, timedelta
from enum import Enum, auto
from typing import Union

from core.events._base import Event
from core.events.meta import EventMeta
from core.result import Result


class Status(Enum):
    SUCCESS = auto()
    FAIL = auto()


@dataclass(frozen=True)
class Command(Event):
    _execution_event: asyncio.Event = field(default_factory=asyncio.Event, init=False)
    _status: Result[Status, Union[Exception, None]] = field(default=None, init=False)
    meta: EventMeta = field(default_factory=lambda: EventMeta(priority=1), init=False)

    def executed(self, status: Result):
        self._execution_event.set()
        object.__setattr__(self, "_status", status)

    async def wait_for_execution(self) -> Result:
        await self._execution_event.wait()
        return self._status

    def __post_init__(self):
        attribute_values = [
            getattr(self, field.name)
            for field in fields(self)
            if field.name not in ["meta", "_execution_event"]
        ]
        expiration = datetime.now() + timedelta(seconds=5)
        concatenated = f"{self.__class__.__name__}{attribute_values}{expiration}"
        idempotency_key = hashlib.sha256(concatenated.encode("utf-8")).hexdigest()

        object.__setattr__(
            self,
            "meta",
            EventMeta(
                priority=self.meta.priority,
                group=self.meta.group,
                version=self.meta.version,
                key=idempotency_key,
            ),
        )
