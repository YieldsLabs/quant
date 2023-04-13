from concurrent.futures import ThreadPoolExecutor
import inspect
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
                 target_metric="total_pnl", num_last_trades=15, hyperparameters=None):
        super().__init__(ohlcv)
        self.broker = broker
        self.analytics = analytics
        self.symbols = symbols
        self.timeframes = timeframes
        self.strategies = self._create_instances(strategies, hyperparameters)
        self.stop_loss_finders = self._create_instances(stop_loss_finders, hyperparameters,  pre_args=(ohlcv,))
        self.take_profit_finders = self._create_instances(take_profit_finders, hyperparameters)
        self.num_last_trades = num_last_trades
        self.target_metric = target_metric

    def _run_backtest(self, settings, rm, analytics):
        symbol, timeframe, strategy, id = settings

        print(f"Backtest: {id}")

        backtester = Backtester(self.ohlcv_context, self.broker, rm, analytics)

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
    
    def _create_instances(self, classes, hyperparameters, pre_args=()):
        instances_dict = {}

        for cls in classes:
            signature = inspect.signature(cls.__init__)
            parameters = signature.parameters

            applicable_hyperparams = {
                param_name: hyperparameters[param_name]
                for param_name in parameters
                if param_name in hyperparameters
            }

            if not applicable_hyperparams:
                instance = cls(*pre_args)
                instances_dict[str(instance)] = instance
            else:
                instance = cls(*pre_args, **applicable_hyperparams)
                instances_dict[str(instance)] = instance

        return list(instances_dict.values())
    
    def _unique_settings(self, seen_ids, risk_manager_keys):
        settings_iter = list(product(self.symbols, self.timeframes, self.strategies, risk_manager_keys))
        random.shuffle(settings_iter)

        for symbol, timeframe, strategy, risk_manager_key in settings_iter:
            current_id = self._generate_id(symbol, timeframe, strategy, risk_manager_key)
            if self._is_unique_id(current_id, seen_ids):
                yield (symbol, timeframe, strategy, risk_manager_key, current_id)

    def run(self):
        risk_manager_dict = {
            (symbol, stop_loss_finder, take_profit_finder): RiskManager(
                stop_loss_finder,
                take_profit_finder,
                **self.broker.get_symbol_info(symbol),
            )
            for symbol in self.symbols
            for stop_loss_finder in self.stop_loss_finders
            for take_profit_finder in self.take_profit_finders
        }

        seen_ids = set()
        risk_manager_keys = list(risk_manager_dict.keys())

        with ThreadPoolExecutor(max_workers=multiprocessing.cpu_count()) as executor:
            results_list = [
                executor.submit(
                    self._run_backtest,
                    (setting[0], setting[1], setting[2], setting[4]),
                    risk_manager_dict[setting[3]],
                    self.analytics
                )
                for setting in self._unique_settings(seen_ids, risk_manager_keys)
            ]
            results_list = [result.result() for result in results_list]

        return pd.DataFrame(results_list).sort_values(
            by=self.target_metric, ascending=False
        )
