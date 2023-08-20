from dataclasses import dataclass, field
from typing import List, Tuple, Type

from backtest.lookback import Lookback
from datasource.abstract_datasource import AbstractDatasource
from strategy_management.abstract_actor import AbstractActor

from .base_event import Event, EventMeta
from ..timeframe import Timeframe


@dataclass(frozen=True)
class BacktestStarted(Event):
    datasource: Type[AbstractDatasource]
    actor: Type[AbstractActor]
    symbols_timeframes: List[Tuple[str, Timeframe]]
    lookback: Lookback
    meta: EventMeta = field(default_factory=lambda: EventMeta(priority=3))
