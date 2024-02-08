from dataclasses import dataclass, field, replace

import numpy as np

TOTAL_TRADES_THRESHOLD = 5


@dataclass(frozen=True)
class Performance:
    _account_size: float
    _risk_per_trade: float
    _periods_per_year: float = 252
    _pnl: np.array = field(default_factory=lambda: np.array([]))

    @property
    def total_trades(self) -> int:
        return self._pnl.size

    @property
    def total_pnl(self) -> float:
        return np.sum(self._pnl)

    @property
    def average_pnl(self) -> float:
        return np.mean(self._pnl)

    @property
    def max_consecutive_wins(self) -> int:
        return self._max_streak(self._pnl, True)

    @property
    def max_consecutive_losses(self) -> int:
        return self._max_streak(self._pnl, False)

    @property
    def hit_ratio(self) -> float:
        pnl_positive = self._pnl > 0
        successful_trades = np.sum(pnl_positive)

        return successful_trades / self.total_trades

    @property
    def sharpe_ratio(self) -> float:
        avg_return = self.average_pnl
        std_return = np.std(self._pnl)

        if std_return == 0:
            return 0

        return avg_return / std_return

    @property
    def equity(self):
        return self._account_size + self._pnl.cumsum()

    @property
    def drawdown(self):
        equity_curve = self.equity
        peak = np.maximum.accumulate(equity_curve)
        drawdowns = (peak - equity_curve) / peak

        return drawdowns

    @property
    def runup(self) -> float:
        equity_curve = self.equity
        trough = np.minimum.accumulate(equity_curve)
        runups = (equity_curve - trough) / trough

        return runups

    @property
    def max_runup(self) -> float:
        return np.max(self.runup)

    @property
    def max_drawdown(self) -> float:
        return np.max(self.drawdown)

    @property
    def calmar_ratio(self) -> float:
        max_drawdown = self.max_drawdown

        if max_drawdown == 0:
            return 0

        rate_of_return = self._rate_of_return(self._account_size, self.total_pnl)

        return rate_of_return / np.abs(max_drawdown)

    @property
    def sortino_ratio(self) -> float:
        downside_returns = self._pnl[self._pnl < 0]

        if len(downside_returns) < 2:
            return 0

        downside_std = np.std(downside_returns)

        if downside_std == 0:
            return 0

        return self.average_pnl / downside_std

    @property
    def cagr(self) -> float:
        periods = self.total_trades

        if periods < TOTAL_TRADES_THRESHOLD:
            return 0

        final_value = self.equity[-1]
        initial_value = self._account_size

        if initial_value == 0:
            return 0

        if final_value < initial_value:
            return -1

        compound_factor = final_value / initial_value
        time_factor = 1 / (periods / self._periods_per_year)

        return np.power(compound_factor, time_factor) - 1

    @property
    def optimal_f(self) -> float:
        if self.total_trades < TOTAL_TRADES_THRESHOLD:
            return self._risk_per_trade

        max_loss = np.min(self.drawdown)

        if max_loss == 0:
            return self._risk_per_trade

        initial_value = self._account_size
        final_value = self.equity[-1]
        growth_factor = final_value / initial_value

        drawdown_fraction = np.abs(max_loss) / np.abs(initial_value)

        geometric_mean = np.sqrt(growth_factor)

        return drawdown_fraction * geometric_mean

    @property
    def kelly(self) -> float:
        if self.total_trades < TOTAL_TRADES_THRESHOLD:
            return self._risk_per_trade

        win_trades = self._pnl[self._pnl > 0]
        loss_trades = self._pnl[self._pnl < 0]

        if len(win_trades) == 0 or len(loss_trades) == 0:
            return self._risk_per_trade

        win_probability = len(win_trades) / self.total_trades
        average_win_to_loss_ratio = np.mean(win_trades) / np.abs(np.mean(loss_trades))

        p = 1 / average_win_to_loss_ratio
        q = 1 - win_probability

        return (win_probability * p - q) / p

    @property
    def annualized_return(self) -> float:
        rate_of_return = self._rate_of_return(self._account_size, self.total_pnl)

        if rate_of_return < 0 and self._periods_per_year % self.total_trades != 0:
            return 0

        holding_period_return = 1 + rate_of_return

        return (
            np.power(holding_period_return, self._periods_per_year / self.total_trades)
            - 1
        )

    @property
    def annualized_volatility(self) -> float:
        if self.total_trades < TOTAL_TRADES_THRESHOLD:
            return 0

        daily_returns = self._pnl / self._account_size
        volatility = np.std(daily_returns, ddof=1)

        return volatility * np.sqrt(self._periods_per_year)

    @property
    def recovery_factor(self) -> float:
        pnl_positive = self._pnl > 0
        total_profit = np.sum(self._pnl[pnl_positive])

        return total_profit / self.max_drawdown if self.max_drawdown != 0 else 0

    @property
    def profit_factor(self) -> float:
        pnl_positive = self._pnl > 0
        gross_profit = np.sum(self._pnl[pnl_positive])
        gross_loss = np.abs(np.sum(self._pnl[~pnl_positive]))

        if gross_loss == 0:
            return 0

        return gross_profit / gross_loss

    @property
    def risk_of_ruin(self) -> float:
        win_rate = self.hit_ratio

        if win_rate == 1 or win_rate == 0:
            return 0

        loss_rate = 1 - win_rate

        return (
            (1 - (self._risk_per_trade * (1 - loss_rate / win_rate)))
            ** self._account_size
        ) * 100

    @property
    def skewness(self) -> float:
        if self.total_trades < TOTAL_TRADES_THRESHOLD:
            return 0

        average_pnl = self.average_pnl
        std_pnl = np.std(self._pnl, ddof=1)

        if std_pnl == 0:
            return 0

        return np.sum(((self._pnl - average_pnl) / std_pnl) ** 3) / self.total_trades

    @property
    def kurtosis(self) -> float:
        if self.total_trades < TOTAL_TRADES_THRESHOLD:
            return 0

        average_pnl = self.average_pnl
        std_pnl = np.std(self._pnl, ddof=1)

        if std_pnl == 0:
            return 0

        return (
            np.sum(((self._pnl - average_pnl) / std_pnl) ** 4) / self.total_trades - 3
        )

    @property
    def var(self, confidence_level=0.95) -> float:
        daily_returns = self._pnl / self._account_size

        return -np.percentile(daily_returns, (1 - confidence_level) * 100)

    @property
    def cvar(self, alpha=0.05) -> float:
        pnl_sorted = np.sort(self._pnl)
        n_losses = int(alpha * len(self._pnl))

        if n_losses == 0:
            return 0

        return -pnl_sorted[:n_losses].mean()

    @property
    def ulcer_index(self) -> float:
        if self.total_trades < TOTAL_TRADES_THRESHOLD:
            return 0

        account_size = self._account_size
        peak = account_size
        drawdowns_squared = []

        for pnl_value in self._pnl:
            account_size += pnl_value
            peak = max(peak, account_size)
            drawdown = (peak - account_size) / peak
            drawdowns_squared.append(drawdown**2)

        return np.sqrt(np.mean(drawdowns_squared))

    @property
    def lake_ratio(self) -> float:
        account_size = self._account_size + self._pnl.cumsum()
        peaks = np.maximum.accumulate(account_size)
        drawdowns = (peaks - account_size) / peaks
        underwater_time = np.sum(drawdowns < 0) / self._periods_per_year

        return 1 - underwater_time

    @property
    def burke_ratio(self) -> float:
        if self.total_trades < TOTAL_TRADES_THRESHOLD:
            return 0

        downside_deviation = np.std(np.minimum(self._pnl, 0), ddof=1)

        if downside_deviation == 0:
            return 0

        return self.cagr / downside_deviation

    @property
    def rachev_ratio(self) -> float:
        if self.total_trades < TOTAL_TRADES_THRESHOLD:
            return 0

        pnl_sorted = np.sort(self._pnl)[::-1]

        var_95 = np.percentile(pnl_sorted, 5)

        shortfall = pnl_sorted[pnl_sorted <= var_95]

        if len(shortfall) == 0:
            return 0

        expected_shortfall = np.abs(np.mean(shortfall))

        if expected_shortfall == 0:
            return 0

        return np.abs(self._pnl.mean()) / expected_shortfall

    @property
    def sterling_ratio(self) -> float:
        if self.total_trades < TOTAL_TRADES_THRESHOLD:
            return 0

        gains = self._pnl[self._pnl > 0]
        losses = self._pnl[self._pnl < 0]

        if len(losses) == 0 or len(gains) == 0:
            return 0

        upside_potential = np.mean(gains)
        downside_risk = np.sqrt(np.mean(losses**2))

        if downside_risk == 0:
            return 0

        return upside_potential / downside_risk

    @property
    def tail_ratio(self) -> float:
        if self.total_trades < TOTAL_TRADES_THRESHOLD:
            return 0

        var_95 = np.percentile(self._pnl, 95)

        gains = self._pnl[self._pnl > var_95]
        losses = self._pnl[self._pnl < np.percentile(self._pnl, 5)]

        if len(losses) == 0 or len(gains) == 0:
            return 0

        gain_tail = np.mean(gains)

        loss_tail = np.mean(losses)

        if np.abs(loss_tail) < np.abs(gain_tail):
            return 0

        return np.abs(gain_tail) / np.abs(loss_tail)

    @property
    def omega_ratio(self) -> float:
        if self.total_trades < TOTAL_TRADES_THRESHOLD:
            return 0

        gains = self._pnl[self._pnl > 0]
        losses = self._pnl[self._pnl < 0]

        if len(losses) == 0 or len(gains) == 0:
            return 0

        sum_losses = np.sum(np.abs(losses))

        if sum_losses == 0:
            return 0

        return np.sum(gains) / sum_losses

    @property
    def kappa_three_ratio(self) -> float:
        gains = self._pnl[self._pnl > 0]
        losses = self._pnl[self._pnl < 0]

        if len(losses) == 0 or len(gains) == 0:
            return 0

        avg_gain = np.mean(gains)
        avg_loss = np.mean(losses)

        threshold = avg_gain - avg_loss

        up_proportion = (gains > threshold).sum() / self.total_trades
        down_proportion = (losses < threshold).sum() / self.total_trades

        return (up_proportion**3 - down_proportion) / np.sqrt(np.mean(self._pnl**2))

    def next(self, pnl: float) -> "Performance":
        _pnl = np.append(self._pnl, pnl)

        return replace(self, _pnl=_pnl)

    @staticmethod
    def _max_streak(pnl, winning: bool) -> int:
        streak = max_streak = 0
        pnl_positive = pnl > 0

        for pnl_value in pnl_positive:
            if pnl_value == winning:
                streak += 1
                max_streak = max(max_streak, streak)
            else:
                streak = 0

        return max_streak

    @staticmethod
    def _rate_of_return(initial_account_size, total_pnl) -> float:
        account_size = initial_account_size + total_pnl

        return (account_size / initial_account_size) - 1

    def __repr__(self):
        return (
            f"Performance(total_trades={self.total_trades}, hit_ratio={self.hit_ratio}, profit_factor={self.profit_factor}, "
            + f"max_runup={self.max_runup}, max_drawdown={self.max_drawdown}, sortino_ratio={self.sortino_ratio}, calmar_ratio={self.calmar_ratio}, "
            + f"risk_of_ruin={self.risk_of_ruin}, recovery_factor={self.recovery_factor}, optimal_f={self.optimal_f}, "
            + f"total_pnl={self.total_pnl}, average_pnl={self.average_pnl}, sharpe_ratio={self.sharpe_ratio}, "
            + f"max_consecutive_wins={self.max_consecutive_wins}, max_consecutive_losses={self.max_consecutive_losses}, "
            + f"cagr={self.cagr}, annualized_return={self.annualized_return}, annualized_volatility={self.annualized_volatility}, "
            + f"var={self.var}, cvar={self.cvar}, ulcer_index={self.ulcer_index}, kelly={self.kelly}, "
            + f"lake_ratio={self.lake_ratio}, burke_ratio={self.burke_ratio}, rachev_ratio={self.rachev_ratio}, kappa_three_ratio={self.kappa_three_ratio}, "
            + f"sterling_ratio={self.sterling_ratio}, tail_ratio={self.tail_ratio}, omega_ratio={self.omega_ratio}, "
            + f"skewness={self.skewness}, kurtosis={self.kurtosis})"
        )

    def to_dict(self):
        return {
            "account_size": self._account_size,
            "total_trades": self.total_trades,
            "total_pnl": self.total_pnl,
            "average_pnl": self.average_pnl,
            "max_consecutive_wins": self.max_consecutive_wins,
            "max_consecutive_losses": self.max_consecutive_losses,
            "hit_ratio": self.hit_ratio,
            "equity": self.equity,
            "runup": self.runup,
            "max_runup": self.max_runup,
            "drawdown": self.drawdown,
            "max_drawdown": self.max_drawdown,
            "sharpe_ratio": self.sharpe_ratio,
            "calmar_ratio": self.calmar_ratio,
            "sortino_ratio": self.sortino_ratio,
            "cagr": self.cagr,
            "optimal_f": self.optimal_f,
            "kelly": self.kelly,
            "annualized_return": self.annualized_return,
            "annualized_volatility": self.annualized_volatility,
            "recovery_factor": self.recovery_factor,
            "profit_factor": self.profit_factor,
            "risk_of_ruin": self.risk_of_ruin,
            "skewness": self.skewness,
            "kurtosis": self.kurtosis,
            "var": self.var,
            "cvar": self.cvar,
            "ulcer_index": self.ulcer_index,
            "lake_ratio": self.lake_ratio,
            "burke_ratio": self.burke_ratio,
            "rachev_ratio": self.rachev_ratio,
            "sterling_ratio": self.sterling_ratio,
            "tail_ratio": self.tail_ratio,
            "omega_ratio": self.omega_ratio,
            "kappa_three_ratio": self.kappa_three_ratio,
        }
