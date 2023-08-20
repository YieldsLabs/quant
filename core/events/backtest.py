from dataclasses import dataclass, field
from typing import Type

from backtest.lookback import Lookback
from datasource.abstract_datasource import AbstractDatasource
from strategy_management.abstract_actor import AbstractActor

from .base_event import Event, EventMeta


@dataclass(frozen=True)
class BacktestStarted(Event):
    datasource: Type[AbstractDatasource]
    actor: Type[AbstractActor]
    lookback: Lookback
    meta: EventMeta = field(default_factory=lambda: EventMeta(priority=4))
