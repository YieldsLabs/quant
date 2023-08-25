from dataclasses import dataclass
from typing import Any, List

from core.interfaces.abstract_executor_factory import AbstractExecutorFactory
from core.models.lookback import Lookback
from core.interfaces.abstract_broker import AbstractBroker
from core.models.timeframe import Timeframe
from core.interfaces.abstract_datasource import AbstractDatasource
from core.interfaces.abstract_ws import AbstractWS


@dataclass
class TradingContext:
    executor_factory: AbstractExecutorFactory
    datasource: AbstractDatasource
    ws_handler: AbstractWS
    broker: AbstractBroker
    timeframes: List[Timeframe]
    strategies: List[List[Any]]
    lookback: Lookback
    batch_size: int
    leverage: int
    live_mode: bool
