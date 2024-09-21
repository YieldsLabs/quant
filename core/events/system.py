from dataclasses import dataclass, field
from typing import List

from core.events.meta import EventMeta
from core.groups.event import EventGroup
from core.models.strategy import Strategy

from ._base import Event


@dataclass(frozen=True)
class SystemEvent(Event):
    meta: EventMeta = field(
        default_factory=lambda: EventMeta(priority=8, group=EventGroup.system),
        init=False,
    )


@dataclass(frozen=True)
class DeployStrategy(SystemEvent):
    strategy: List[Strategy]
