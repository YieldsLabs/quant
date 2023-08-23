from dataclasses import dataclass, field
from typing import Type

from .base_event import Event, EventMeta

from ..interfaces.abstract_datasource import AbstractDatasource
from ..models.lookback import Lookback
from ..models.strategy import Strategy



@dataclass(frozen=True)
class BacktestStarted(Event):
    datasource: Type[AbstractDatasource]
    strategy: Strategy
    lookback: Lookback
    meta: EventMeta = field(default_factory=lambda: EventMeta(priority=9))
