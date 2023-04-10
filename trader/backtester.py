from enum import Enum
from typing import Type
import pandas as pd
from analytics.abstract_performace import AbstractPerformance
from broker.abstract_broker import AbstractBroker
from ohlcv.context import OhlcvContext, update_ohlcv
from risk_management.abstract_risk_manager import AbstractRiskManager
from shared.order import Order
from shared.timeframes import Timeframes
from trader.trade_type import TradeType
from strategy.abstract_strategy import AbstractStrategy
from trader.abstract_trader import AbstractTrader
from shared.position_side import PositionSide


class SignalType(Enum):
    LONG = 'long'
    SHORT = 'short'


class Backtester(AbstractTrader):
    def __init__(self, ohlcv: Type[OhlcvContext], broker: Type[AbstractBroker], risk_management: Type[AbstractRiskManager], analytics: Type[AbstractPerformance], trade_type=TradeType.BOTH, initial_account_size=1000, window_size=100):
        super().__init__(ohlcv)
        self.broker = broker
        self.risk_management = risk_management
        self.initial_account_size = initial_account_size
        self.analytics = analytics
        self.trade_type = trade_type
        self.window_size = window_size
        self.orders = []

    @update_ohlcv
    def trade(self, strategy: Type[AbstractStrategy], symbol: str, timeframe: Timeframes):
        long_signals, short_signals = self._generate_signals(strategy)
        return self._calculate_performance(long_signals, short_signals)

    def _generate_signals(self, strategy):
        ohlcv = self.ohlcv_context.ohlcv

        n_rows = len(ohlcv)
        
        long_signals = []
        short_signals = []

        for i in range(n_rows - self.window_size + 1):
            window_data = ohlcv.iloc[i:i + self.window_size]
            long_signal, short_signal = strategy.entry(window_data)

            if long_signal:
                long_signals.append(window_data.iloc[-1])
            if short_signal:
                short_signals.append(window_data.iloc[-1])

        return pd.DataFrame(long_signals), pd.DataFrame(short_signals)

    def _calculate_performance(self, long_signals, short_signals):
        long_signals['signal'], short_signals['signal'] = SignalType.LONG, SignalType.SHORT

        combined_signals = pd.concat([long_signals, short_signals]).sort_index()

        trades = []
        active_trade = None

        for index, row in self.ohlcv_context.ohlcv.iterrows():
            signal_row = combined_signals.loc[combined_signals.index == index]

            if not signal_row.empty:
                signal_type = signal_row.iloc[0]['signal']

                if active_trade is None:
                    if signal_type == SignalType.LONG and (self.trade_type == TradeType.BOTH or self.trade_type == TradeType.LONG):
                        active_trade = (PositionSide.LONG, row)

                    if signal_type == SignalType.SHORT and (self.trade_type == TradeType.BOTH or self.trade_type == TradeType.SHORT):
                        active_trade = (PositionSide.SHORT, row)

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
        for entry_trade, exit_trade in zip(trades[::2], trades[1::2]):
            
            entry_price, exit_price = entry_trade[1]['close'], exit_trade[1]['close']
            timestamp = exit_trade[1]['timestamp']

            position_size, stop_loss_price, take_profit_price = self.risk_management.calculate_entry(entry_trade[0], self.initial_account_size, entry_price)

            profit = self.risk_management.calculate_profit(entry_trade[0], position_size, entry_price, exit_price, take_profit_price, stop_loss_price)

            self.orders.append(Order(timestamp=timestamp, side=entry_trade[0], entry_price=entry_price, exit_price=exit_price, stop_loss=stop_loss_price, take_profit=take_profit_price, pnl=profit))

        return self.analytics.calculate(self.orders)

    def get_orders(self):
        return pd.DataFrame.from_records([order.to_dict() for order in self.orders])
