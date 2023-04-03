from itertools import product
from typing import List, Type

import pandas as pd
from analytics.performance import PerformanceStats
from broker.abstract_broker import AbstractBroker
from risk_management.stop_loss.base.abstract_stop_loss_finder import AbstractStopLoss
from risk_management.take_profit.abstract_take_profit_finder import AbstractTakeProfit
from shared.ohlcv_context import OhlcvContext
from strategy.abstract_strategy import AbstractStrategy
from trader.backtester import Backtester
from market.abstract_screening import AbstractScreening
from risk_management.risk_manager import RiskManager

class StrategyScreening(AbstractScreening):
    def __init__(self, ohlcv: Type[OhlcvContext], broker: Type[AbstractBroker], analytics: Type[PerformanceStats], symbols: List[str], timeframes: List[str], strategies: List[AbstractStrategy], stop_loss_finders: List[AbstractStopLoss], take_profit_finders: List[AbstractTakeProfit], lookback=5000, num_last_trades=15):
        super().__init__(ohlcv)
        self.broker = broker
        self.analytics = analytics
        self.symbols = symbols
        self.timeframes = timeframes
        self.strategies = strategies
        self.stop_loss_finders = stop_loss_finders
        self.take_profit_finders = take_profit_finders
        self.num_last_trades = num_last_trades
        self.lookback = lookback

    def run(self):
        results_list = []
        for symbol, timeframe, strategy, stop_loss_finder, take_profit_finder in product(
            self.symbols, self.timeframes, self.strategies, self.stop_loss_finders, self.take_profit_finders
        ):
            market = self.broker.get_symbol_info(symbol)

            trading_fee, price_precision, position_precision = market[
                'trading_fee'], market['price_precision'], market['position_precision']

            rm = RiskManager(
                stop_loss_finder,
                take_profit_finder,
                trading_fee=trading_fee,
                price_precision=price_precision,
                position_precision=position_precision,
            )

            backtester = Backtester(self.ohlcv_context, self.broker, rm, self.analytics)
            
            result = backtester.trade(strategy, symbol, timeframe)

            result.update({
                'symbol': symbol,
                'timeframe': timeframe,
                'strategy': strategy,
                'stop_loss_finder': stop_loss_finder,
                'take_profit_finder': take_profit_finder,
                'win_rate': result['win_rate'] * 100,
            })

            results_list.append(result)

            print(f"{symbol} orders for strategy: {strategy}, TimeFrame: {timeframe}, StopLossFinder: {stop_loss_finder}, TakeProfitFinder: {take_profit_finder}")
            print(backtester.get_orders().tail(self.num_last_trades))

        return pd.DataFrame(results_list).sort_values(by="total_pnl", ascending=False)
