
import numpy as np
import pandas as pd
from shared.trade_type import TradeType

class Order:
    def __init__(self, side, entry_price, exit_price, stop_loss, take_profit, profit):
        self.side = side
        self.entry_price = entry_price
        self.exit_price = exit_price
        self.stop_loss = stop_loss
        self.take_profit = take_profit
        self.profit = profit

    def to_dict(self):
        return {
            'side': self.side,
            'entry': self.entry_price,
            'exit': self.exit_price,
            'profit': self.profit,
            'stop loss': self.stop_loss,
            'take profit': self.take_profit,
        }
        
class Backtester:
    def __init__(self, strategy, risk_management, historical_data, initial_account_size=1000, leverage=1):
        self.strategy = strategy
        self.historical_data = historical_data
        self.initial_account_size = initial_account_size
        self.leverage = leverage
        self.risk_management = risk_management
        self.equity_curve = []
        self.orders = []


    def run(self, trade_type=TradeType.BOTH):
        data_with_indicators = self.strategy.add_indicators(
            self.historical_data)
        long_signals, short_signals = self.generate_signals(
            data_with_indicators)
        
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

            if not signal_row.empty:
                signal_type = signal_row.iloc[0]['signal']

                if active_trade is None:
                    if signal_type == 'long' and (trade_type == TradeType.BOTH or trade_type == TradeType.LONG):
                        active_trade = (TradeType.LONG, row)

                    if signal_type == 'short' and (trade_type == TradeType.BOTH or trade_type == TradeType.SHORT):
                        active_trade = (TradeType.SHORT, row)

                elif active_trade is not None:
                    entry_trade_type, entry_row = active_trade
                    entry_price = entry_row['close']

                    if self.risk_management.check_exit_conditions(entry_trade_type, entry_price, row):
                        trades.append(active_trade)
                        trades.append(('exit', row))
                        active_trade = None

        if active_trade is not None:
            trades.append(active_trade)
            trades.append(('exit', self.historical_data.iloc[-1]))

        performance_stats = self.evaluate_trades(trades)
        return performance_stats

    def evaluate_trades(self, trades):
        total_trades = 0
        successful_trades = 0
        account_size = self.initial_account_size
        win_streak = 0
        loss_streak = 0
        max_consecutive_wins = 0
        max_consecutive_losses = 0
        max_drawdown = 0
        peak = self.initial_account_size

        for i in range(0, len(trades), 2):
            if i + 1 >= len(trades):
                break

            entry_trade, exit_trade = trades[i], trades[i + 1]
            entry_price, exit_price = entry_trade[1]['close'], exit_trade[1]['close']
            profit = 0

            if entry_trade[0] == TradeType.LONG:
                stop_loss_price, take_profit_price = self.risk_management.calculate_prices(entry_trade[0], entry_price)
                position_size = self.risk_management.calculate_position_size(account_size, entry_price, stop_loss_price)

                profit = (exit_price - entry_price) * position_size
                self.orders.append(Order(side=entry_trade[0], entry_price=entry_price, exit_price=exit_price, stop_loss=stop_loss_price, take_profit=take_profit_price, profit=profit))

            elif entry_trade[0] == TradeType.SHORT:
                stop_loss_price, take_profit_price = self.risk_management.calculate_prices(entry_trade[0], entry_price)
                position_size = self.risk_management.calculate_position_size(account_size, entry_price, stop_loss_price)

                profit = (entry_price - exit_price) * position_size
                
                self.orders.append(Order(side=entry_trade[0], entry_price=entry_price, exit_price=exit_price, take_profit=take_profit_price, stop_loss=stop_loss_price, profit=profit))

            if profit > 0:
                win_streak += 1
                loss_streak = 0
                max_consecutive_wins = max(max_consecutive_wins, win_streak)
            else:
                loss_streak += 1
                win_streak = 0
                max_consecutive_losses = max(max_consecutive_losses, loss_streak)

            account_size += profit
            self.equity_curve.append(account_size)

            peak = max(peak, account_size)
            drawdown = (peak - account_size) / peak
            max_drawdown = max(max_drawdown, drawdown)
        
        total_trades = len(self.orders)
        successful_trades = len([order for order in self.orders if order.profit > 0])
        pnl = [order.profit for order in self.orders]
        win_rate = successful_trades / total_trades if total_trades > 0 else 0
        total_pnl = np.sum(pnl) if len(pnl) else 0
        average_pnl = np.mean(pnl) if len(pnl) else 0
        sharpe_ratio = self.calculate_sharpe_ratio(pnl) if len(pnl) else 0
        rate_of_return = (account_size / self.initial_account_size) - 1

        return {
            'total_trades': total_trades,
            'successful_trades': successful_trades,
            'win_rate': win_rate,
            'rate_of_return': rate_of_return,
            'total_pnl': total_pnl,
            'average_pnl': average_pnl,
            'sharpe_ratio': sharpe_ratio,
            'max_consecutive_wins': max_consecutive_wins,
            'max_consecutive_losses': max_consecutive_losses,
            'max_drawdown': max_drawdown
        }

    def calculate_sharpe_ratio(self, pnl, risk_free_rate=0):
        pnl_array = np.array(pnl)
        avg_return = np.mean(pnl_array)
        std_return = np.std(pnl_array)

        if std_return == 0:
            return np.nan

        sharpe_ratio = (avg_return - risk_free_rate) / std_return
        return sharpe_ratio

    def get_signals(self):
        data_with_indicators = self.strategy.add_indicators(
            self.historical_data)
        return self.generate_signals(
            data_with_indicators)

    def get_equity_curve(self):
        return self.equity_curve

    def get_orders(self):
        return pd.DataFrame.from_records([order.to_dict() for order in self.orders])
