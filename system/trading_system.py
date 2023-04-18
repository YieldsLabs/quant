from typing import List, Type
from analytics.abstract_analytics import AbstractAnalytics
from core.timeframe import Timeframe
from datasource.abstract_datasource import AbstractDatasource
from journal.log_journal import LogJournal
from portfolio_management.portfolio_manager import PortfolioManager
from risk_management.risk_manager import RiskManager
from strategy.abstract_strategy import AbstractStrategy
from strategy.strategy_manager import StrategyManager
from system.abstract_system import AbstractSystem
from optimization.backtest import Backtest
from trader.live_trader import LiveTrader
from trader.paper_trader import PaperTrader


class TradingSystem(AbstractSystem):
    def __init__(self, datasource: Type[AbstractDatasource], analytics: Type[AbstractAnalytics], symbols: List[str], timeframes: List[Timeframe], strategies: List[AbstractStrategy], leverage=1, lookback=5000, risk_per_trade=0.001):
        super().__init__()
        self.symbols = symbols
        self.timeframes = timeframes
        self.leverage = leverage
        self.lookback = lookback

        self.portfolio_manager = PortfolioManager(datasource=datasource, analytics=analytics, risk_per_trade=risk_per_trade)
        self.risk_manager = RiskManager(trailing_stop_loss=False)
        self.backtest = Backtest(datasource)
        self.strategy_manager = StrategyManager([cls() for cls in strategies])
        self.journal = LogJournal()
        self.trader = None

    def start(self):
        self.run_backtest()

    def run_backtest(self):
        self.trader = PaperTrader()
        self.backtest.run(self.symbols, self.timeframes, lookback=self.lookback)
    
    def run_trading(self):
        self.trader = LiveTrader()