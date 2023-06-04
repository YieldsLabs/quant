from typing import Type

from analytics.abstract_analytics import AbstractAnalytics
from broker.abstract_broker import AbstractBroker
from datasource.abstract_datasource import AbstractDatasource
from datasource.abstract_ws import AbstractWS
from optimization.abstract_optimization import AbstractOptimization
from optimization.backtest import Backtest, Lookback
from portfolio_management.portfolio_manager import PortfolioManager
from risk_management.risk_manager import RiskManager


class TradingContext:
    def __init__(self, datasource: Type[AbstractDatasource], ws_handler: Type[AbstractWS], broker: Type[AbstractBroker], analytics: Type[AbstractAnalytics], optimization: Type[AbstractOptimization], lookback: Lookback, leverage: int, risk_per_trade: float, live_mode: bool):
        self.datasource = datasource
        self.ws_handler = ws_handler
        self.broker = broker
        self.optimization = optimization
        self.analytics = analytics
        self.leverage = leverage
        self.lookback = lookback
        self.risk_per_trade = risk_per_trade
        self.live_mode = live_mode

        self.portfolio_manager = PortfolioManager(datasource, self.leverage, self.risk_per_trade)
        self.risk_manager = RiskManager()
        self.backtest = Backtest(datasource)
