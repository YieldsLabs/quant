from dataclasses import dataclass, field

from core.events.base import Event, EventGroup, EventMeta
from core.models.strategy import StrategyType


@dataclass(frozen=True)
class SystemEvent(Event):
    meta: EventMeta = field(
        default_factory=lambda: EventMeta(priority=8, group=EventGroup.system),
        init=False,
    )


@dataclass(frozen=True)
class UpdatedStrategy(SystemEvent):
    type: StrategyType
