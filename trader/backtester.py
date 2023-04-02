
from typing import Type
import pandas as pd
from analytics.performance import PerformanceStats
from risk_management.abstract_risk_manager import AbstractRiskManager
from shared.ohlcv_context import OhlcvContext
from shared.order import Order
from shared.trade_type import TradeType
from strategy.abstract_strategy import AbstractStrategy
from trader.abstract_trader import AbstractTrader

class Backtester(AbstractTrader):
    def __init__(self, ohlcv: Type[OhlcvContext], risk_management: Type[AbstractRiskManager], analytics: Type[PerformanceStats], trade_type=TradeType.BOTH, initial_account_size=1000):
        super().__init__(ohlcv)
        self.risk_management = risk_management
        self.initial_account_size = initial_account_size
        self.analytics = analytics
        self.trade_type = trade_type
        self.orders = []

    def trade(self, strategy: Type[AbstractStrategy], symbol: str, timeframe: str):
        long_signals, short_signals = self._generate_signals(strategy)
        
        return self._calculate_performance(long_signals, short_signals)

    def _generate_signals(self, strategy):
        go_long = []
        go_short = []
        for index, row in self.ohlcv_context.ohlcv.iterrows():
            long_signal, short_signal = strategy.entry(self.ohlcv_context.ohlcv[:index])
            
            if long_signal:
                go_long.append(row)
            if short_signal:
                go_short.append(row)

        return pd.DataFrame(go_long), pd.DataFrame(go_short)

    def _calculate_performance(self, long_signals, short_signals):
        if self.trade_type == TradeType.LONG:
            short_signals = pd.DataFrame()
        elif self.trade_type == TradeType.SHORT:
            long_signals = pd.DataFrame()

        long_signals['signal'] = 'long'
        short_signals['signal'] = 'short'
        
        combined_signals = pd.concat([long_signals, short_signals]).sort_index()

        trades = []
        active_trade = None

        for index, row in self.ohlcv_context.ohlcv.iterrows():
            signal_row = combined_signals.loc[combined_signals.index == index]

            if not signal_row.empty:
                signal_type = signal_row.iloc[0]['signal']

                if active_trade is None:
                    if signal_type == 'long' and (self.trade_type == TradeType.BOTH or self.trade_type == TradeType.LONG):
                        active_trade = (TradeType.LONG, row)

                    if signal_type == 'short' and (self.trade_type == TradeType.BOTH or self.trade_type == TradeType.SHORT):
                        active_trade = (TradeType.SHORT, row)

                else:
                    entry_trade_type, entry_row = active_trade
                    entry_price = entry_row['close']

                    if self.risk_management.check_exit_conditions(entry_trade_type, entry_price, row):
                        trades.append(active_trade)
                        trades.append(('exit', row))
                        active_trade = None

        if active_trade is not None:
            trades.append(active_trade)
            trades.append(('exit', self.ohlcv_context.ohlcv.iloc[-1]))

        return self._evaluate_trades(trades)

    def _evaluate_trades(self, trades):
        for i in range(0, len(trades), 2):
            if i + 1 >= len(trades):
                break

            entry_trade, exit_trade = trades[i], trades[i + 1]
            entry_price, exit_price = entry_trade[1]['close'], exit_trade[1]['close']
            profit = 0

            stop_loss_price, take_profit_price = self.risk_management.calculate_prices(entry_trade[0], entry_price)
            position_size = self.risk_management.calculate_position_size(self.initial_account_size, entry_price, stop_loss_price)

            if entry_trade[0] == TradeType.LONG:
                exit_price = min(exit_price, take_profit_price if take_profit_price else exit_price)
                exit_price = max(exit_price, stop_loss_price if stop_loss_price else stop_loss_price) 

                profit = (exit_price - entry_price) * position_size

            elif entry_trade[0] == TradeType.SHORT:
                exit_price = max(exit_price, take_profit_price if take_profit_price else exit_price)
                exit_price = min(exit_price, stop_loss_price if stop_loss_price else stop_loss_price)
                
                profit = (entry_price - exit_price) * position_size
                
            self.orders.append(Order(timestamp=exit_trade[1]['timestamp'], side=entry_trade[0], entry_price=entry_price, exit_price=exit_price, stop_loss=stop_loss_price, take_profit=take_profit_price, profit=profit))

        return self.analytics.calculate(self.orders)


    def get_orders(self):
        return pd.DataFrame.from_records([order.to_dict() for order in self.orders])
