from concurrent.futures import ThreadPoolExecutor
from itertools import product
from typing import List, Type

import pandas as pd
from analytics.abstract_performace import AbstractPerformance
from broker.abstract_broker import AbstractBroker
from ohlcv.context import OhlcvContext
from optimization.abstract_screening import AbstractScreening
from risk_management.stop_loss.base.abstract_stop_loss_finder import AbstractStopLoss
from risk_management.take_profit.abstract_take_profit_finder import AbstractTakeProfit
from strategy.abstract_strategy import AbstractStrategy
from trader.backtester import Backtester
from risk_management.risk_manager import RiskManager


class StrategyScreening(AbstractScreening):
    def __init__(self, ohlcv: Type[OhlcvContext], broker: Type[AbstractBroker], analytics: Type[AbstractPerformance], symbols: List[str], timeframes: List[str], strategies: List[AbstractStrategy], stop_loss_finders: List[AbstractStopLoss], take_profit_finders: List[AbstractTakeProfit], num_last_trades=15):
        super().__init__(ohlcv)
        self.broker = broker
        self.analytics = analytics
        self.symbols = symbols
        self.timeframes = timeframes
        self.strategies = strategies
        self.stop_loss_finders = stop_loss_finders
        self.take_profit_finders = take_profit_finders
        self.num_last_trades = num_last_trades

    def _run_backtest(self, settings, rm):
        symbol, timeframe, strategy = settings

        backtester = Backtester(self.ohlcv_context, self.broker, rm, self.analytics)

        result = backtester.trade(strategy, symbol, timeframe)
        label = f"{symbol}_{timeframe}{strategy}{rm.stop_loss_finder}{rm.take_profit_finder}"
        
        result.update({ 'label': label })
        
        print(backtester.get_orders().tail(self.num_last_trades))
        return result

    def run(self):
        market_dict = {symbol: self.broker.get_symbol_info(symbol) for symbol in self.symbols}

        risk_manager_dict = {(symbol, stop_loss_finder, take_profit_finder): RiskManager(stop_loss_finder, take_profit_finder, **market_dict[symbol]) for symbol in self.symbols for stop_loss_finder, take_profit_finder in product(self.stop_loss_finders, self.take_profit_finders)}

        combined_settings = list(product(self.symbols, self.timeframes, self.strategies, risk_manager_dict.keys()))

        with ThreadPoolExecutor() as executor:
            results_list = [executor.submit(self._run_backtest, settings[:3], risk_manager_dict[settings[0], settings[3][1], settings[3][2]]) for settings in combined_settings]
            results_list = [result.result() for result in results_list]

        return pd.DataFrame(results_list).sort_values(by="total_pnl", ascending=False)
