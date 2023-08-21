from dataclasses import dataclass
from typing import Any, List, Type

from backtest.lookback import Lookback
from broker.abstract_broker import AbstractBroker
from core.timeframe import Timeframe
from datasource.abstract_datasource import AbstractDatasource
from datasource.abstract_ws import AbstractWS
from portfolio_management.abstract_portfolio_manager import AbstractPortfolioManager
from strategy_management.abstract_strategy_factory import AbstractStrategyActorFactory


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
