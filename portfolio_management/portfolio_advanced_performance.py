import numpy as np

from core.events.portfolio import AdvancedPortfolioPerformance


class PortfolioAdvancedPerformance:
    def __init__(self, periods_per_year: int = 252):
        self.periods_per_year = periods_per_year

    def next(self, positions, initial_account_size) -> AdvancedPortfolioPerformance:
        total_trades = len(positions)

        if total_trades == 0:
            return AdvancedPortfolioPerformance(0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0)
        
        pnl = np.array([position.pnl for position in positions])
        
        sharpe_ratio = self._sharpe_ratio(pnl)
        sortino_ratio = self._sortino_ratio(pnl)
        lake_ratio = self._lake_ratio(pnl, initial_account_size, self.periods_per_year)
        burke_ratio = self._burke_ratio(pnl, initial_account_size, self.periods_per_year)
        rachev_ratio = self._rachev_ratio(pnl)
        tail_ratio = self._tail_ratio(pnl)
        omega_ratio = self._omega_ratio(pnl)
        sterling_ratio = self._sterling_ratio(pnl)
        kappa_three_ratio = self._kappa_three_ratio(pnl)
        profit_factor = self._profit_factor(pnl)
        skewness = self._skewness(pnl)
        kurtosis = self._kurtosis(pnl)
        var = self._var(pnl, initial_account_size)
        cvar = self._cvar(pnl)
        ulcer_index = self._ulcer_index(pnl, initial_account_size)
       
        return AdvancedPortfolioPerformance(
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
            skewness=skewness,
            kurtosis=kurtosis,
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

        if periods < 2 or initial_account_size <= 0 or account_size[-1] <= 0:
            return 0

        ratio = account_size[-1] / initial_account_size

        if ratio <= 0:
            return 0

        cagr = ratio ** (periods_per_year / periods) - 1

        downside_deviation = np.std(np.minimum(pnl, 0), ddof=1)

        if downside_deviation == 0:
            return 0

        burke_ratio = cagr / downside_deviation

        return burke_ratio
    
    @staticmethod
    def _profit_factor(pnl) -> float:
        pnl_positive = pnl > 0
        gross_profit = pnl[pnl_positive].sum()
        gross_loss = np.abs(pnl[~pnl_positive].sum())

        if gross_loss == 0:
            return 0

        return gross_profit / gross_loss
    

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

