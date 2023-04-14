from dataclasses import asdict, dataclass
from typing import List
import numpy as np

from analytics.abstract_performace import AbstractPerformance
from shared.order import Order

@dataclass
class PerformanceStatsResults:
    total_trades: int
    successful_trades: int
    win_rate: float
    risk_of_ruin: float
    rate_of_return: float
    total_pnl: float
    average_pnl: float
    sharpe_ratio: float
    sortino_ratio: float
    profit_factor: float
    max_consecutive_wins: int
    max_consecutive_losses: int
    max_drawdown: float
    recovery_factor: float

    def to_dict(self):
        return asdict(self)


class PerformanceStats(AbstractPerformance):
    def __init__(self, initial_account_size: float, risk_per_trade: float):
        super().__init__()
        self.initial_account_size = initial_account_size
        self.risk_per_trade = risk_per_trade

    def calculate(self, orders: List[Order]) -> PerformanceStatsResults:
        pnl = [order.pnl for order in orders]
        total_trades = len(orders)
        successful_trades = sum(order.pnl > 0 for order in orders)
        max_drawdown = self._max_drawdown(pnl) if pnl else 0
        win_rate = successful_trades / total_trades if total_trades else 0

        return PerformanceStatsResults(
            total_trades=total_trades,
            successful_trades=successful_trades,
            win_rate=win_rate,
            risk_of_ruin=self._risk_of_ruin(win_rate),
            rate_of_return=self._rate_of_return(pnl),
            total_pnl=np.sum(pnl) if pnl else 0,
            average_pnl=np.mean(pnl) if pnl else 0,
            sharpe_ratio=self._sharpe_ratio(pnl) if pnl else 0,
            sortino_ratio=self._sortino_ratio(pnl) if pnl else 0,
            profit_factor=self._profit_factor(pnl) if pnl else 0,
            max_consecutive_wins=self._max_streak(pnl, True),
            max_consecutive_losses=self._max_streak(pnl, False),
            max_drawdown=max_drawdown,
            recovery_factor=self._recovery_factor(pnl, max_drawdown) if pnl else 0
        )

    def _sharpe_ratio(self, pnl, risk_free_rate=0):
        pnl_array = np.array(pnl)
        avg_return = np.mean(pnl_array)
        std_return = np.std(pnl_array)

        return (avg_return - risk_free_rate) / std_return if std_return else np.nan
    
    def _sortino_ratio(self, pnl, risk_free_rate=0):
        pnl_array = np.array(pnl)
        downside_returns = pnl_array[pnl_array < 0]

        if len(downside_returns) < 2:
            return 0

        downside_std = np.std(downside_returns)

        if downside_std == 0:
            return 0
        
        avg_return = np.mean(pnl_array)
        sortino_ratio = (avg_return - risk_free_rate) / downside_std

        return sortino_ratio

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
    
    def _profit_factor(self, pnl):
        pnl_array = np.array(pnl)
        gross_profit = np.sum(pnl_array[pnl_array > 0])
        gross_loss = np.abs(np.sum(pnl_array[pnl_array < 0]))

        if gross_loss == 0:
            return np.nan

        profit_factor = gross_profit / gross_loss
        return profit_factor

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
    
    def _recovery_factor(self, pnl, max_drawdown):
        total_profit = sum(pnl_value for pnl_value in pnl if pnl_value > 0)
        
        return total_profit / max_drawdown if max_drawdown != 0 else 0
    
    def _risk_of_ruin(self, win_rate: float):
        if win_rate == 1 or win_rate == 0:
            return 0

        loss_rate = 1 - win_rate
        risk_of_ruin = ((1 - (self.risk_per_trade * (1 - loss_rate / win_rate))) ** self.initial_account_size) * 100
        
        return risk_of_ruin