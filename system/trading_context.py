from typing import List, Type
from analytics.abstract_analytics import AbstractAnalytics
from broker.abstract_broker import AbstractBroker
from core.timeframe import Timeframe
from datasource.abstract_datasource import AbstractDatasource
from optimization.backtest import Backtest
from portfolio_management.portfolio_manager import PortfolioManager
from risk_management.risk_manager import RiskManager
from strategy_management.abstract_strategy import AbstractStrategy
from strategy_management.kmeans_inference import KMeansInference
from strategy_management.strategy_manager import StrategyManager


class TradingContext:
    def __init__(self, datasource: Type[AbstractDatasource], broker: Type[AbstractBroker], analytics: Type[AbstractAnalytics], inference: Type[KMeansInference], strategies: List[AbstractStrategy], symbols: List[str], timeframes: List[Timeframe], lookback: int, leverage: int, risk_per_trade: float, subscribe: callable):
        self.datasource = datasource
        self.broker = broker
        self.analytics = analytics
        self.strategies = strategies
        self.symbols = symbols
        self.timeframes = timeframes
        self.lookback = lookback
        self.risk_per_trade = risk_per_trade
        self.subscribe = subscribe

        self.portfolio_manager = PortfolioManager(datasource, analytics, leverage, risk_per_trade)
        self.risk_manager = RiskManager()
        self.backtest = Backtest(datasource)
        self.strategy_manager = StrategyManager(strategies, inference)
