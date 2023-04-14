from enum import Enum
import time
from typing import Type
import numpy as np
import pandas as pd
from analytics.abstract_performace import AbstractPerformance
from analytics.performance import PerformanceStatsResults
from ohlcv.context import update_ohlcv
from risk_management.abstract_risk_manager import AbstractRiskManager
from shared.order import Order
from shared.timeframes import Timeframes
from trader.trade_type import TradeType
from strategy.base.abstract_strategy import AbstractStrategy
from trader.abstract_trader import AbstractTrader
from shared.position_side import PositionSide


class SignalType(Enum):
    LONG = 'long'
    SHORT = 'short'


invervals = {
    Timeframes.ONE_MINUTE: 20 * 5,
    Timeframes.THREE_MINUTES: 20 * 5,
    Timeframes.FIVE_MINUTES: 18 * 5,
    Timeframes.FIFTEEN_MINUTES: 18 * 5,
    Timeframes.ONE_HOUR: 24 * 5,
    Timeframes.FOUR_HOURS: 30 * 5,
}


class Backtester(AbstractTrader):
    def __init__(self, risk_management: Type[AbstractRiskManager], analytics: Type[AbstractPerformance], trade_type=TradeType.BOTH, initial_account_size=1000):
        super().__init__()
        self.risk_management = risk_management
        self.initial_account_size = initial_account_size
        self.analytics = analytics
        self.trade_type = trade_type
        self.orders = []

    @update_ohlcv
    def trade(self, strategy: Type[AbstractStrategy], symbol: str, timeframe: Timeframes):
        long_signals, short_signals = self._generate_signals(strategy, invervals[timeframe])
        return self._calculate_performance(long_signals, short_signals)

    def _generate_signals(self, strategy, interval):
        ohlcv = self.ohlcv_context.ohlcv
        n_rows = len(ohlcv)
        window_size = interval - 1

        long_signals = np.zeros(n_rows, dtype=bool)
        short_signals = np.zeros(n_rows, dtype=bool)

        for i in range(window_size, n_rows):
            window_data = ohlcv.iloc[i - window_size:i + 1]
            long_signal, short_signal = strategy.entry(window_data)

            long_signals[i] = long_signal
            short_signals[i] = short_signal

        return np.where(long_signals)[0].tolist(), np.where(short_signals)[0].tolist()

    def _calculate_performance(self, long_signals, short_signals):
        long_signals, short_signals = pd.DataFrame(long_signals), pd.DataFrame(short_signals)
        long_signals['signal'], short_signals['signal'] = SignalType.LONG, SignalType.SHORT

        combined_signals = pd.concat([long_signals, short_signals]).sort_index()

        trades = []
        active_trade = None

        signal_idx = combined_signals.index.isin(self.ohlcv_context.ohlcv.index)
        signal_rows = combined_signals[signal_idx]

        for index, row in signal_rows.iterrows():
            signal_type, ohlcv = row['signal'], self.ohlcv_context.ohlcv.loc[index]

            if active_trade is None:
                if signal_type == SignalType.LONG and (self.trade_type == TradeType.BOTH or self.trade_type == TradeType.LONG):
                    active_trade = (PositionSide.LONG, ohlcv)

                if signal_type == SignalType.SHORT and (self.trade_type == TradeType.BOTH or self.trade_type == TradeType.SHORT):
                    active_trade = (PositionSide.SHORT, ohlcv)

            else:
                entry_trade_type, entry_row = active_trade
                entry_price = entry_row['close']

                if self.risk_management.check_exit_conditions(entry_trade_type, entry_price, ohlcv):
                    trades.append(active_trade)
                    trades.append(('exit', ohlcv))
                    active_trade = None

        if active_trade is not None:
            trades.append(active_trade)
            trades.append(('exit', self.ohlcv_context.ohlcv.iloc[-1]))

        return self._evaluate_trades(trades)

    def _evaluate_trades(self, trades) -> PerformanceStatsResults:
        for entry_trade, exit_trade in zip(trades[::2], trades[1::2]):

            entry_price, exit_price = entry_trade[1]['close'], exit_trade[1]['close']
            timestamp = exit_trade[1]['timestamp']

            position_size, stop_loss_price, take_profit_price = self.risk_management.calculate_entry(entry_trade[0], self.initial_account_size, entry_price)

            profit = self.risk_management.calculate_profit(entry_trade[0], position_size, entry_price, exit_price, take_profit_price, stop_loss_price)

            self.orders.append(Order(timestamp=timestamp, side=entry_trade[0], entry_price=entry_price, exit_price=exit_price, stop_loss=stop_loss_price, take_profit=take_profit_price, pnl=profit))

        return self.analytics.calculate(self.orders)

    def get_orders(self):
        return pd.DataFrame.from_records([order.to_dict() for order in self.orders])
