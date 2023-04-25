from typing import List
import numpy as np
from .abstract_analytics import AbstractAnalytics
from core.events.portfolio import PortfolioPerformance
from core.position import Position


class StrategyPerformance(AbstractAnalytics):
    def __init__(self, risk_per_trade: float = 0.001, periods_per_year: int = 252):
        super().__init__()
        self.risk_per_trade = risk_per_trade
        self.periods_per_year = periods_per_year

    def calculate(self, initial_account_size: float, positions: List[Position]) -> PortfolioPerformance:
        total_trades = len(positions)

        if total_trades == 0:
            return PortfolioPerformance(
                total_trades=0,
                successful_trades=0,
                win_rate=0,
                risk_of_ruin=0,
                rate_of_return=0,
                annualized_return=0,
                annualized_volatility=0,
                total_pnl=0,
                average_pnl=0,
                sharpe_ratio=0,
                sortino_ratio=0,
                lake_ratio=0,
                burke_ratio=0,
                profit_factor=0,
                max_consecutive_wins=0,
                max_consecutive_losses=0,
                max_drawdown=0,
                recovery_factor=0,
                skewness=0,
                kurtosis=0,
                calmar_ratio=0,
                var=0,
                cvar=0,
                ulcer_index=0
            )

        pnl = np.array([position.calculate_pnl() for position in positions])

        pnl_positive = pnl > 0
        successful_trades = pnl_positive.sum()
        win_rate = successful_trades / total_trades
        risk_of_ruin = self._risk_of_ruin(win_rate, initial_account_size)
        rate_of_return = self._rate_of_return(pnl, initial_account_size)
        total_pnl = pnl.sum()
        average_pnl = pnl.mean()
        sharpe_ratio = self._sharpe_ratio(pnl)
        sortino_ratio = self._sortino_ratio(pnl)
        lake_ratio = self._lake_ratio(pnl, initial_account_size)
        burke_ratio = self._burke_ratio(pnl, initial_account_size)
        profit_factor = self._profit_factor(pnl, pnl_positive)
        max_consecutive_wins = self._max_streak(pnl_positive, True)
        max_consecutive_losses = self._max_streak(pnl_positive, False)
        max_drawdown = self._max_drawdown(pnl, initial_account_size)
        recovery_factor = self._recovery_factor(total_pnl, max_drawdown)
        calmar_ratio = self._calmar_ratio(rate_of_return, max_drawdown)
        var = self._var(pnl, initial_account_size)
        cvar = self._cvar(pnl)
        ulcer_index = self._ulcer_index(pnl, initial_account_size)
        annualized_volatility = self._annualized_volatility(pnl, initial_account_size)
        annualized_return = self._annualized_return(rate_of_return, total_trades)

        skewness = self._skewness(pnl)
        kurtosis = self._kurtosis(pnl)

        return PortfolioPerformance(
            total_trades=total_trades,
            successful_trades=successful_trades,
            win_rate=win_rate,
            risk_of_ruin=risk_of_ruin,
            rate_of_return=rate_of_return,
            annualized_return=annualized_return,
            annualized_volatility=annualized_volatility,
            total_pnl=total_pnl,
            average_pnl=average_pnl,
            sharpe_ratio=sharpe_ratio,
            sortino_ratio=sortino_ratio,
            lake_ratio=lake_ratio,
            burke_ratio=burke_ratio,
            profit_factor=profit_factor,
            max_consecutive_wins=max_consecutive_wins,
            max_consecutive_losses=max_consecutive_losses,
            max_drawdown=max_drawdown,
            recovery_factor=recovery_factor,
            skewness=skewness,
            kurtosis=kurtosis,
            calmar_ratio=calmar_ratio,
            var=var,
            cvar=cvar,
            ulcer_index=ulcer_index
        )

    def _sharpe_ratio(self, pnl, risk_free_rate=0):
        avg_return = np.mean(pnl)
        std_return = np.std(pnl)

        if std_return == 0:
            return 0

        return (avg_return - risk_free_rate) / std_return

    def _sortino_ratio(self, pnl, risk_free_rate=0):
        downside_returns = pnl[pnl < 0]

        if len(downside_returns) < 2:
            return 0

        downside_std = np.std(downside_returns)

        if downside_std == 0:
            return 0

        avg_return = np.mean(pnl)
        sortino_ratio = (avg_return - risk_free_rate) / downside_std

        return sortino_ratio

    def _max_streak(self, pnl_positive, winning: bool):
        streak = max_streak = 0

        for pnl_value in pnl_positive:
            if pnl_value == winning:
                streak += 1
                max_streak = max(max_streak, streak)
            else:
                streak = 0

        return max_streak

    def _rate_of_return(self, pnl, initial_account_size):
        account_size = initial_account_size + pnl.sum()

        return (account_size / initial_account_size) - 1

    def _profit_factor(self, pnl, pnl_positive):
        gross_profit = pnl[pnl_positive].sum()
        gross_loss = np.abs(pnl[~pnl_positive].sum())

        if gross_loss == 0:
            return 0

        return gross_profit / gross_loss

    def _max_drawdown(self, pnl, initial_account_size):
        account_size = initial_account_size
        peak = account_size
        max_drawdown = 0

        for pnl_value in pnl:
            account_size += pnl_value
            peak = max(peak, account_size)
            drawdown = (peak - account_size) / peak
            max_drawdown = max(max_drawdown, drawdown)

        return max_drawdown

    def _recovery_factor(self, pnl, max_drawdown):
        total_profit = pnl[pnl > 0].sum()

        return total_profit / max_drawdown if max_drawdown != 0 else 0

    def _risk_of_ruin(self, win_rate: float, initial_account_size: float):
        if win_rate == 1 or win_rate == 0:
            return 0

        loss_rate = 1 - win_rate

        risk_of_ruin = ((1 - (self.risk_per_trade * (1 - loss_rate / win_rate))) ** initial_account_size) * 100

        return risk_of_ruin

    def _skewness(self, pnl):
        n = len(pnl)

        if n < 3:
            return 0

        mean_pnl = np.mean(pnl)
        std_pnl = np.std(pnl, ddof=1)

        if std_pnl == 0:
            return 0

        skewness = np.sum(((pnl - mean_pnl) / std_pnl) ** 3) / n

        return skewness

    def _kurtosis(self, pnl):
        n = len(pnl)

        if n < 4:
            return 0

        mean_pnl = np.mean(pnl)
        std_pnl = np.std(pnl, ddof=1)

        if std_pnl == 0:
            return 0

        excess_kurtosis = np.sum(((pnl - mean_pnl) / std_pnl) ** 4) / n - 3

        return excess_kurtosis

    def _calmar_ratio(self, rate_of_return: float, max_drawdown: float) -> float:
        if max_drawdown == 0:
            return 0

        calmar_ratio = rate_of_return / abs(max_drawdown)

        return calmar_ratio

    def _var(self, pnl, initial_account_size, confidence_level=0.95) -> float:
        daily_returns = pnl / initial_account_size
        value_at_risk = -np.percentile(daily_returns, (1 - confidence_level) * 100)

        return value_at_risk

    def _cvar(self, pnl, alpha=0.05):
        pnl_sorted = np.sort(pnl)
        n_losses = int(alpha * len(pnl))

        if n_losses == 0:
            return 0

        cvar = -pnl_sorted[:n_losses].mean()

        return cvar

    def _ulcer_index(self, pnl, initial_account_size):
        if len(pnl) == 0:
            return 0

        account_size = initial_account_size
        peak = account_size
        drawdowns_squared = []

        for pnl_value in pnl:
            account_size += pnl_value
            peak = max(peak, account_size)
            drawdown = (peak - account_size) / peak
            drawdowns_squared.append(drawdown ** 2)

        ulcer_index = np.sqrt(np.mean(drawdowns_squared))

        return ulcer_index

    def _annualized_volatility(self, pnl, initial_account_size) -> float:
        total_periods = len(pnl)
        if total_periods < 2:
            return 0

        daily_returns = pnl / initial_account_size
        volatility = np.std(daily_returns, ddof=1)
        annualized_volatility = volatility * np.sqrt(self.periods_per_year)

        return annualized_volatility

    def _annualized_return(self, rate_of_return: float, total_trades: int) -> float:
        holding_period_return = 1 + rate_of_return
        annualized_return = holding_period_return ** (self.periods_per_year / total_trades) - 1

        return annualized_return

    def _lake_ratio(self, pnl: np.ndarray, initial_account_size: float) -> float:
        account_size = initial_account_size + pnl.cumsum()
        peaks = np.maximum.accumulate(account_size)
        drawdowns = (peaks - account_size) / peaks
        underwater_time = np.sum(drawdowns < 0) / self.periods_per_year
        lake_ratio = 1 - underwater_time

        return lake_ratio

    def _burke_ratio(self, pnl, initial_account_size: float) -> float:
        account_size = initial_account_size + pnl.cumsum()
        periods = len(pnl)
        cagr = (account_size[-1] / initial_account_size) ** (self.periods_per_year / periods) - 1
        downside_deviation = np.std(np.minimum(pnl, 0), ddof=1)
        burke_ratio = cagr / downside_deviation

        return burke_ratio
