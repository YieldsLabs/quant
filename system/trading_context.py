from dataclasses import dataclass
from typing import List, Type

from backtest.lookback import Lookback
from broker.abstract_broker import AbstractBroker
from core.timeframe import Timeframe
from datasource.abstract_datasource import AbstractDatasource
from datasource.abstract_ws import AbstractWS
from portfolio_management.abstract_portfolio_manager import AbstractPortfolioManager
from strategy_management.abstract_strategy_factory import AbsctractStrategyActorFactory


@dataclass
class TradingContext:
    strategy_factory: Type[AbsctractStrategyActorFactory]
    datasource: Type[AbstractDatasource]
    ws_handler: Type[AbstractWS]
    broker: Type[AbstractBroker]
    portfolio: Type[AbstractPortfolioManager]
    timeframes: List[Timeframe]
    lookback: Lookback
    leverage: int
    live_mode: bool
