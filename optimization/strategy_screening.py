from concurrent.futures import ThreadPoolExecutor
from itertools import product
import random
from typing import List, Type

import multiprocessing
import pandas as pd
from analytics.abstract_performace import AbstractPerformance
from broker.abstract_broker import AbstractBroker
from ohlcv.context import OhlcvContext
from optimization.abstract_screening import AbstractScreening
from risk_management.stop_loss.base.abstract_stop_loss_finder import AbstractStopLoss
from risk_management.take_profit.abstract_take_profit_finder import AbstractTakeProfit
from strategy.base.abstract_strategy import AbstractStrategy
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

    def _generate_id(self, symbol, timeframe, strategy, rm):
        _, stop_loss, take_profit = rm
        return f"{symbol}_{timeframe}{strategy}{stop_loss}{take_profit}"
    
    def _unique_settings(self, seen_ids, risk_manager_keys):
        settings_iter = list(product(self.symbols, self.timeframes, self.strategies, risk_manager_keys))
        random.shuffle(settings_iter)
        for symbol, timeframe, strategy, risk_manager_key in settings_iter:
            current_id = self._generate_id(symbol, timeframe, strategy, risk_manager_key)
            if self._is_unique_id(current_id, seen_ids):
                yield (symbol, timeframe, strategy, risk_manager_key, current_id)


    def run(self):
        market_dict = {symbol: self.broker.get_symbol_info(symbol) for symbol in self.symbols}
        risk_manager_products = product(self.stop_loss_finders, self.take_profit_finders)

        risk_manager_dict = {
            (symbol, stop_loss_finder, take_profit_finder): RiskManager(
                stop_loss_finder,
                take_profit_finder,
                **market_dict[symbol],
            )
            for symbol in self.symbols
            for stop_loss_finder, take_profit_finder in risk_manager_products
        }

        seen_ids = set()
        risk_manager_keys = list(risk_manager_dict.keys())

        with ThreadPoolExecutor(max_workers=multiprocessing.cpu_count()) as executor:
            results_list = [
                executor.submit(
                    self._run_backtest,
                    (setting[0], setting[1], setting[2], setting[4]),
                    risk_manager_dict[setting[3]],
                )
                for setting in self._unique_settings(seen_ids, risk_manager_keys)
            ]
            results_list = [result.result() for result in results_list]

        return pd.DataFrame(results_list).sort_values(
            by=self.sort_by, ascending=False
        )
