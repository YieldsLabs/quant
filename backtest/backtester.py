
import pandas as pd
from shared.order import Order
from shared.trade_type import TradeType

class Backtester:
    def __init__(self, strategy, risk_management, analytics, historical_data, initial_account_size=1000, leverage=1):
        self.strategy = strategy
        self.historical_data = historical_data
        self.initial_account_size = initial_account_size
        self.leverage = leverage
        self.risk_management = risk_management
        self.analytics = analytics
        self.orders = []

    def run(self, trade_type=TradeType.BOTH):
        long_signals, short_signals = self.generate_signals(self.historical_data)
        
        return self.calculate_performance(long_signals, short_signals, trade_type=trade_type)

    def generate_signals(self, data):
        go_long = []
        go_short = []

        for index, row in data.iterrows():
            long_signal, short_signal = self.strategy.entry(
                data.iloc[:index])
            if long_signal:
                go_long.append(row)
            if short_signal:
                go_short.append(row)

        return pd.DataFrame(go_long), pd.DataFrame(go_short)

    def calculate_performance(self, long_signals, short_signals, trade_type=TradeType.BOTH):
        if trade_type == TradeType.LONG:
            short_signals = pd.DataFrame()
        elif trade_type == TradeType.SHORT:
            long_signals = pd.DataFrame()

        long_signals['signal'] = 'long'
        short_signals['signal'] = 'short'
        
        combined_signals = pd.concat([long_signals, short_signals]).sort_index()

        trades = []
        active_trade = None

        for index, row in self.historical_data.iterrows():
            signal_row = combined_signals.loc[combined_signals.index == index]

            if not signal_row.empty and active_trade is None:
                signal_type = signal_row.iloc[0]['signal']

                if signal_type == 'long' and (trade_type == TradeType.BOTH or trade_type == TradeType.LONG):
                    active_trade = (TradeType.LONG, row)

                if signal_type == 'short' and (trade_type == TradeType.BOTH or trade_type == TradeType.SHORT):
                    active_trade = (TradeType.SHORT, row)

            if active_trade is not None:
                entry_trade_type, entry_row = active_trade
                entry_price = entry_row['close']

                if self.risk_management.check_exit_conditions(entry_trade_type, entry_price, row):
                    trades.append(active_trade)
                    trades.append(('exit', row))
                    active_trade = None

        if active_trade is not None:
            trades.append(active_trade)
            trades.append(('exit', self.historical_data.iloc[-1]))

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
                exit_price = min(exit_price, take_profit_price)
                exit_price = max(exit_price, stop_loss_price) 

                profit = (exit_price - entry_price) * position_size

            elif entry_trade[0] == TradeType.SHORT:
                exit_price = max(exit_price, take_profit_price)
                exit_price = min(exit_price, stop_loss_price)
                
                profit = (entry_price - exit_price) * position_size
                
            self.orders.append(Order(side=entry_trade[0], entry_price=entry_price, exit_price=exit_price, stop_loss=stop_loss_price, take_profit=take_profit_price, profit=profit))

        return self.analytics.calculate(self.orders)

    def get_signals(self):
        data_with_indicators = self.strategy.add_indicators(
            self.historical_data)
        return self.generate_signals(
            data_with_indicators)

    def get_orders(self):
        return pd.DataFrame.from_records([order.to_dict() for order in self.orders])
