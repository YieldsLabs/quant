from typing import List
import numpy as np
from .abstract_analytics import AbstractAnalytics
from core.events.portfolio import PortfolioPerformance
from core.position import Position


class StrategyPerformance(AbstractAnalytics):
    def __init__(self, account_size: float = 1000, risk_per_trade: float = 0.001, periods_per_year: int = 252):
        super().__init__()
        self.account_size = account_size
        self.risk_per_trade = risk_per_trade
        self.periods_per_year = periods_per_year

    def calculate(self, positions: List[Position]) -> PortfolioPerformance:
        initial_account_size = self.account_size
        risk_per_trade = self.risk_per_trade
        periods_per_year = self.periods_per_year

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
                rachev_ratio=0,
                tail_ratio=0,
                omega_ratio=0,
                sterling_ratio=0,
                kappa_three_ratio=0,
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
        risk_of_ruin = self._risk_of_ruin(win_rate, initial_account_size, risk_per_trade)
        rate_of_return = self._rate_of_return(pnl, initial_account_size)
        total_pnl = pnl.sum()
        average_pnl = pnl.mean()
        sharpe_ratio = self._sharpe_ratio(pnl)
        sortino_ratio = self._sortino_ratio(pnl)
        lake_ratio = self._lake_ratio(pnl, initial_account_size, periods_per_year)
        burke_ratio = self._burke_ratio(pnl, initial_account_size, periods_per_year)
        rachev_ratio = self._rachev_ratio(pnl)
        tail_ratio = self._tail_ratio(pnl)
        omega_ratio = self._omega_ratio(pnl)
        sterling_ratio = self._sterling_ratio(pnl)
        kappa_three_ratio = self._kappa_three_ratio(pnl)
        profit_factor = self._profit_factor(pnl, pnl_positive)
        max_consecutive_wins = self._max_streak(pnl_positive, True)
        max_consecutive_losses = self._max_streak(pnl_positive, False)
        max_drawdown = self._max_drawdown(pnl, initial_account_size)
        recovery_factor = self._recovery_factor(total_pnl, max_drawdown)
        calmar_ratio = self._calmar_ratio(rate_of_return, max_drawdown)
        var = self._var(pnl, initial_account_size)
        cvar = self._cvar(pnl)
        ulcer_index = self._ulcer_index(pnl, initial_account_size)
        annualized_volatility = self._annualized_volatility(pnl, initial_account_size, periods_per_year)
        annualized_return = self._annualized_return(rate_of_return, total_trades, periods_per_year)

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
            rachev_ratio=rachev_ratio,
            tail_ratio=tail_ratio,
            omega_ratio=omega_ratio,
            sterling_ratio=sterling_ratio,
            kappa_three_ratio=kappa_three_ratio,
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

    @staticmethod
    def _sharpe_ratio(pnl, risk_free_rate=0) -> float:
        avg_return = np.mean(pnl)
        std_return = np.std(pnl)

        if std_return == 0:
            return 0

        return (avg_return - risk_free_rate) / std_return

    @staticmethod
    def _sortino_ratio(pnl, risk_free_rate=0) -> float:
        downside_returns = pnl[pnl < 0]

        if len(downside_returns) < 2:
            return 0

        downside_std = np.std(downside_returns)

        if downside_std == 0:
            return 0

        avg_return = np.mean(pnl)
        sortino_ratio = (avg_return - risk_free_rate) / downside_std

        return sortino_ratio

    @staticmethod
    def _max_streak(pnl_positive, winning: bool) -> int:
        streak = max_streak = 0

        for pnl_value in pnl_positive:
            if pnl_value == winning:
                streak += 1
                max_streak = max(max_streak, streak)
            else:
                streak = 0

        return max_streak

    @staticmethod
    def _rate_of_return(pnl, initial_account_size) -> float:
        account_size = initial_account_size + pnl.sum()

        return (account_size / initial_account_size) - 1

    @staticmethod
    def _profit_factor(pnl, pnl_positive) -> float:
        gross_profit = pnl[pnl_positive].sum()
        gross_loss = np.abs(pnl[~pnl_positive].sum())

        if gross_loss == 0:
            return 0

        return gross_profit / gross_loss

    @staticmethod
    def _max_drawdown(pnl, initial_account_size) -> float:
        account_size = initial_account_size
        peak = account_size
        max_drawdown = 0

        for pnl_value in pnl:
            account_size += pnl_value
            peak = max(peak, account_size)
            drawdown = (peak - account_size) / peak
            max_drawdown = max(max_drawdown, drawdown)

        return max_drawdown

    @staticmethod
    def _recovery_factor(pnl, max_drawdown) -> float:
        total_profit = pnl[pnl > 0].sum()

        return total_profit / max_drawdown if max_drawdown != 0 else 0

    @staticmethod
    def _risk_of_ruin(win_rate: float, initial_account_size: float, risk_per_trade: float) -> float:
        if win_rate == 1 or win_rate == 0:
            return 0

        loss_rate = 1 - win_rate

        risk_of_ruin = ((1 - (risk_per_trade * (1 - loss_rate / win_rate))) ** initial_account_size) * 100

        return risk_of_ruin

    @staticmethod
    def _skewness(pnl) -> float:
        n = len(pnl)

        if n < 3:
            return 0

        mean_pnl = np.mean(pnl)
        std_pnl = np.std(pnl, ddof=1)

        if std_pnl == 0:
            return 0

        skewness = np.sum(((pnl - mean_pnl) / std_pnl) ** 3) / n

        return skewness

    @staticmethod
    def _kurtosis(pnl) -> float:
        n = len(pnl)

        if n < 4:
            return 0

        mean_pnl = np.mean(pnl)
        std_pnl = np.std(pnl, ddof=1)

        if std_pnl == 0:
            return 0

        excess_kurtosis = np.sum(((pnl - mean_pnl) / std_pnl) ** 4) / n - 3

        return excess_kurtosis

    @staticmethod
    def _calmar_ratio(rate_of_return: float, max_drawdown: float) -> float:
        if max_drawdown == 0:
            return 0

        calmar_ratio = rate_of_return / abs(max_drawdown)

        return calmar_ratio

    @staticmethod
    def _var(pnl, initial_account_size, confidence_level=0.95) -> float:
        daily_returns = pnl / initial_account_size
        value_at_risk = -np.percentile(daily_returns, (1 - confidence_level) * 100)

        return value_at_risk

    @staticmethod
    def _cvar(pnl, alpha=0.05) -> float:
        pnl_sorted = np.sort(pnl)
        n_losses = int(alpha * len(pnl))

        if n_losses == 0:
            return 0

        cvar = -pnl_sorted[:n_losses].mean()

        return cvar

    @staticmethod
    def _ulcer_index(pnl, initial_account_size) -> float:
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

    @staticmethod
    def _annualized_volatility(pnl, initial_account_size, periods_per_year: int) -> float:
        total_periods = len(pnl)

        if total_periods < 2:
            return 0

        daily_returns = pnl / initial_account_size
        volatility = np.std(daily_returns, ddof=1)
        annualized_volatility = volatility * np.sqrt(periods_per_year)

        return annualized_volatility

    @staticmethod
    def _annualized_return(rate_of_return: float, total_trades: int, periods_per_year: int) -> float:
        if rate_of_return < 0 and periods_per_year % total_trades != 0:
            return 0
        
        holding_period_return = 1 + rate_of_return
        annualized_return = holding_period_return ** (periods_per_year / total_trades) - 1

        return annualized_return

    @staticmethod
    def _lake_ratio(pnl, initial_account_size: float, periods_per_year: int) -> float:
        account_size = initial_account_size + pnl.cumsum()
        peaks = np.maximum.accumulate(account_size)
        drawdowns = (peaks - account_size) / peaks
        underwater_time = np.sum(drawdowns < 0) / periods_per_year
        lake_ratio = 1 - underwater_time

        return lake_ratio

    @staticmethod
    def _burke_ratio(pnl, initial_account_size: float, periods_per_year: int) -> float:
        account_size = initial_account_size + pnl.cumsum()
        periods = len(pnl)

        if periods < 2:
            return 0

        cagr = (account_size[-1] / initial_account_size) ** (periods_per_year / periods) - 1

        downside_deviation = np.std(np.minimum(pnl, 0), ddof=1)

        if downside_deviation == 0:
            return 0

        burke_ratio = cagr / downside_deviation

        return burke_ratio

    @staticmethod
    def _rachev_ratio(pnl) -> float:
        if len(pnl) < 3:
            return 0

        pnl_sorted = np.sort(pnl)[::-1]

        var_95 = np.percentile(pnl_sorted, 5)

        shortfall = pnl_sorted[pnl_sorted <= var_95]

        if len(shortfall) == 0:
            return 0

        expected_shortfall = np.abs(np.mean(shortfall))

        if expected_shortfall == 0:
            return 0

        rachev_ratio = np.abs(pnl.mean()) / expected_shortfall

        return rachev_ratio

    @staticmethod
    def _tail_ratio(pnl) -> float:
        if len(pnl) < 3:
            return 0

        var_95 = np.percentile(pnl, 95)

        gains = pnl[pnl > var_95]
        losses = pnl[pnl < np.percentile(pnl, 5)]

        if len(losses) == 0 or len(gains) == 0:
            return 0

        gain_tail = np.mean(gains)

        loss_tail = np.mean(losses)

        if np.abs(loss_tail) < np.abs(gain_tail):
            return 0

        tail_ratio = np.abs(gain_tail) / np.abs(loss_tail)

        return tail_ratio

    @staticmethod
    def _omega_ratio(pnl, risk_free_rate: float = 0) -> float:
        if len(pnl) < 3:
            return 0

        gains = pnl[pnl > 0]
        losses = pnl[pnl < 0]

        if len(losses) == 0 or len(gains) == 0:
            return 0

        sum_losses = np.sum(np.abs(losses))

        if sum_losses == 0:
            return 0

        omega_ratio = np.sum(gains) / sum_losses

        omega_ratio -= risk_free_rate

        return omega_ratio

    @staticmethod
    def _sterling_ratio(pnl, risk_free_rate: float = 0) -> float:
        if len(pnl) < 3:
            return 0

        gains = pnl[pnl > 0]
        losses = pnl[pnl < 0]

        if len(losses) == 0 or len(gains) == 0:
            return 0

        upside_potential = np.mean(gains)
        downside_risk = np.sqrt(np.mean(losses ** 2))

        if downside_risk == 0:
            return 0

        sterling_ratio = (upside_potential - risk_free_rate) / downside_risk

        return sterling_ratio

    @staticmethod
    def _kappa_three_ratio(pnl) -> float:
        gains = pnl[pnl > 0]
        losses = pnl[pnl < 0]

        if len(losses) == 0 or len(gains) == 0:
            return 0

        avg_gain = np.mean(gains)
        avg_loss = np.mean(losses)

        threshold = avg_gain - avg_loss

        up_proportion = (gains > threshold).sum() / len(pnl)
        down_proportion = (losses < threshold).sum() / len(pnl)

        kappa_three_ratio = (up_proportion ** 3 - down_proportion) / np.sqrt(np.mean(pnl ** 2))

        return kappa_three_ratio
