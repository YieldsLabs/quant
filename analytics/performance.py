from typing import List
import numpy as np

from analytics.abstract_performace import AbstractPerformance
from shared.order import Order

class PerformanceStats(AbstractPerformance):
    def __init__(self, initial_account_size: float):
        super().__init__()
        self.initial_account_size = initial_account_size
        self.equity = [initial_account_size]

    def calculate(self, orders: List[Order]):
        total_trades = len(orders)
        successful_trades = len(
            [order for order in orders if order.profit > 0])
        pnl = [order.profit for order in orders]
        win_rate = successful_trades / total_trades if total_trades > 0 else 0
        total_pnl = np.sum(pnl) if len(pnl) else 0
        average_pnl = np.mean(pnl) if len(pnl) else 0
        sharpe_ratio = self._calculate_sharpe_ratio(pnl) if len(pnl) else 0
        rate_of_return, max_drawdown, max_consecutive_wins, max_consecutive_losses = self._calculate_drawdown_and_streaks(orders)

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

    def _calculate_sharpe_ratio(self, pnl, risk_free_rate=0):
        pnl_array = np.array(pnl)
        avg_return = np.mean(pnl_array)
        std_return = np.std(pnl_array)

        if std_return == 0:
            return np.nan

        sharpe_ratio = (avg_return - risk_free_rate) / std_return
        return sharpe_ratio

    def _calculate_drawdown_and_streaks(self, orders):
        account_size = self.initial_account_size
        win_streak = 0
        loss_streak = 0
        max_consecutive_wins = 0
        max_consecutive_losses = 0
        max_drawdown = 0
        peak = self.initial_account_size

        for order in orders:
            profit = order.profit
            account_size += profit
            self.equity.append(account_size)

            peak = max(peak, account_size)
            drawdown = (peak - account_size) / peak
            max_drawdown = max(max_drawdown, drawdown)

            if profit > 0:
                win_streak += 1
                loss_streak = 0
                max_consecutive_wins = max(max_consecutive_wins, win_streak)
            else:
                loss_streak += 1
                win_streak = 0
                max_consecutive_losses = max(
                    max_consecutive_losses, loss_streak)

        rate_of_return = (account_size / self.initial_account_size) - 1
        return rate_of_return, max_drawdown, max_consecutive_wins, max_consecutive_losses
