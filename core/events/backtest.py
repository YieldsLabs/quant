from dataclasses import dataclass, field
from typing import Type

from .base_event import Event, EventMeta

from ..interfaces.abstract_datasource import AbstractDatasource
from ..interfaces.abstract_actor import AbstractActor
from ..models.lookback import Lookback


@dataclass(frozen=True)
class BacktestStarted(Event):
    datasource: Type[AbstractDatasource]
    actor: Type[AbstractActor]
    lookback: Lookback
    meta: EventMeta = field(default_factory=lambda: EventMeta(priority=4))
