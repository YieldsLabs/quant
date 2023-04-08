from concurrent.futures import ThreadPoolExecutor
from itertools import product
import random
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
    def __init__(self, ohlcv: Type[OhlcvContext], broker: Type[AbstractBroker], analytics: Type[AbstractPerformance],
                 symbols: List[str], timeframes: List[str], strategies: List[AbstractStrategy],
                 stop_loss_finders: List[AbstractStopLoss], take_profit_finders: List[AbstractTakeProfit],
                 sort_by="total_pnl", num_last_trades=15):
        super().__init__(ohlcv)
        self.broker = broker
        self.analytics = analytics
        self.symbols = symbols
        self.timeframes = timeframes
        self.strategies = strategies
        self.stop_loss_finders = stop_loss_finders
        self.take_profit_finders = take_profit_finders
        self.num_last_trades = num_last_trades
        self.sort_by = sort_by

    def _run_backtest(self, settings, rm):
        symbol, timeframe, strategy, id = settings

        print(f"Backtest: {id}")

        backtester = Backtester(self.ohlcv_context, self.broker, rm, self.analytics)
        result = backtester.trade(strategy, symbol, timeframe)
        result.update({'id': id})

        print(backtester.get_orders().tail(self.num_last_trades))
        return result

    def _is_unique_id(self, id, seen_ids):
        if id in seen_ids:
            return False
        seen_ids.add(id)
        return True

    def _generate_id(self, symbol, timeframe, strategy, risk_manager_tuple):
        return f"{symbol}_{timeframe}{strategy}{risk_manager_tuple[1]}{risk_manager_tuple[2]}"

    def run(self):
        market_dict = {symbol: self.broker.get_symbol_info(symbol) for symbol in self.symbols}
        risk_manager_dict = {(symbol, stop_loss_finder, take_profit_finder): RiskManager(stop_loss_finder, take_profit_finder, **market_dict[symbol]) for symbol in self.symbols for stop_loss_finder, take_profit_finder in product(self.stop_loss_finders, self.take_profit_finders)}

        combined_settings = list(product(self.symbols, self.timeframes, self.strategies, risk_manager_dict.keys()))
        seen_ids = set()
        unique_settings = [(symbol, timeframe, strategy, risk_manager_tuple, self._generate_id(symbol, timeframe, strategy, risk_manager_tuple)) for symbol, timeframe, strategy, risk_manager_tuple in combined_settings if self._is_unique_id(self._generate_id(symbol, timeframe, strategy, risk_manager_tuple), seen_ids)]

        random.shuffle(unique_settings)

        with ThreadPoolExecutor() as executor:
            results_list = [executor.submit(self._run_backtest, (setting[0], setting[1], setting[2], setting[4]), risk_manager_dict[setting[0], setting[3][1], setting[3][2]]) for setting in unique_settings]
            results_list = [result.result() for result in results_list]

        return pd.DataFrame(results_list).sort_values(by=self.sort_by, ascending=False)
