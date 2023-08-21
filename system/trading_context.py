from dataclasses import dataclass
from typing import Any, List, Type

from core.models.lookback import Lookback
from core.interfaces.abstract_broker import AbstractBroker
from core.models.timeframe import Timeframe
from core.interfaces.abstract_datasource import AbstractDatasource
from core.interfaces.abstract_ws import AbstractWS
from core.interfaces.abstract_portfolio_manager import AbstractPortfolioManager
from core.interfaces.abstract_strategy_factory import AbstractStrategyActorFactory


@dataclass
class TradingContext:
    strategy_factory: Type[AbstractStrategyActorFactory]
    datasource: Type[AbstractDatasource]
    ws_handler: Type[AbstractWS]
    broker: Type[AbstractBroker]
    portfolio: Type[AbstractPortfolioManager]
    timeframes: List[Timeframe]
    strategies: List[List[Any]]
    lookback: Lookback
    leverage: int
    live_mode: bool
