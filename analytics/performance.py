from dataclasses import asdict, dataclass
from typing import List, Type
import numpy as np

from analytics.abstract_performace import AbstractPerformance
from shared.order import Order

@dataclass
class PerformanceStatsResults:
    total_trades: int
    successful_trades: int
    win_rate: float
    rate_of_return: float
    total_pnl: float
    average_pnl: float
    sharpe_ratio: float
    max_consecutive_wins: int
    max_consecutive_losses: int
    max_drawdown: float

    def to_dict(self):
        return asdict(self)


class PerformanceStats(AbstractPerformance):
    def __init__(self, initial_account_size: float):
        super().__init__()
        self.initial_account_size = initial_account_size

    def calculate(self, orders: List[Order]) -> PerformanceStatsResults:
        pnl = [order.pnl for order in orders]
        total_trades = len(orders)
        successful_trades = sum(order.pnl > 0 for order in orders)

        return PerformanceStatsResults(
            total_trades=total_trades,
            successful_trades=successful_trades,
            win_rate=successful_trades / total_trades if total_trades else 0,
            rate_of_return=self._rate_of_return(pnl),
            total_pnl=np.sum(pnl) if pnl else 0,
            average_pnl=np.mean(pnl) if pnl else 0,
            sharpe_ratio=self._sharpe_ratio(pnl) if pnl else 0,
            max_consecutive_wins=self._max_streak(pnl, True),
            max_consecutive_losses=self._max_streak(pnl, False),
            max_drawdown=self._max_drawdown(pnl),
        )

    def _sharpe_ratio(self, pnl, risk_free_rate=0):
        pnl_array = np.array(pnl)
        avg_return = np.mean(pnl_array)
        std_return = np.std(pnl_array)

        return (avg_return - risk_free_rate) / std_return if std_return else np.nan

    def _max_streak(self, pnl, winning: bool):
        streak = max_streak = 0
        for pnl_value in pnl:
            if (pnl_value > 0) == winning:
                streak += 1
                max_streak = max(max_streak, streak)
            else:
                streak = 0
        return max_streak

    def _rate_of_return(self, pnl):
        account_size = self.initial_account_size + sum(pnl)
        return (account_size / self.initial_account_size) - 1

    def _max_drawdown(self, pnl):
        account_size = self.initial_account_size
        peak = account_size
        max_drawdown = 0

        for pnl_value in pnl:
            account_size += pnl_value
            peak = max(peak, account_size)
            drawdown = (peak - account_size) / peak
            max_drawdown = max(max_drawdown, drawdown)

        return max_drawdown