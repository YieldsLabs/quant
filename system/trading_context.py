from dataclasses import dataclass
from typing import Any, List

from core.interfaces.abstract_datasource import AbstractDatasource
from core.interfaces.abstract_executor_factory import AbstractExecutorFactory
from core.interfaces.abstract_signal_actor_factory import AbstractSignalActorFactory
from core.models.lookback import Lookback
from core.models.timeframe import Timeframe


@dataclass
class TradingContext:
    datasource: AbstractDatasource
    signal_factory: AbstractSignalActorFactory
    executor_factory: AbstractExecutorFactory
    timeframes: List[Timeframe]
    strategies: List[List[Any]]
    lookback: Lookback
    batch_size: int
    leverage: int
    live_mode: bool
