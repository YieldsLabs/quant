from dataclasses import dataclass
from typing import Any, List

from core.interfaces.abstract_datasource import AbstractDatasource
from core.interfaces.abstract_executor_actor_factory import AbstractExecutorActorFactory
from core.interfaces.abstract_position_actor_factory import AbstractPositionActorFactory
from core.interfaces.abstract_risk_actor_factory import AbstractRiskActorFactory
from core.interfaces.abstract_signal_actor_factory import AbstractSignalActorFactory
from core.models.lookback import Lookback
from core.models.timeframe import Timeframe


@dataclass
class TradingContext:
    datasource: AbstractDatasource
    signal_factory: AbstractSignalActorFactory
    executor_factory: AbstractExecutorActorFactory
    position_factory: AbstractPositionActorFactory
    risk_factory: AbstractRiskActorFactory
    timeframes: List[Timeframe]
    strategy_path: str
    strategies: List[List[Any]]
    blacklist: List[str]
    lookback: Lookback
    batch_size: int
    leverage: int
    live_mode: bool
