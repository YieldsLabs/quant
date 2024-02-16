from dataclasses import dataclass, field, replace

import numpy as np
from scipy.stats import kurtosis, norm, skew

TOTAL_TRADES_THRESHOLD = 3


@dataclass(frozen=True)
class Performance:
    _account_size: float
    _risk_per_trade: float
    _periods_per_year: float = 252
    _pnl: np.array = field(default_factory=lambda: np.array([]))
    _fee: np.array = field(default_factory=lambda: np.array([]))

    @property
    def total_trades(self) -> int:
        return self._pnl.size

    @property
    def total_pnl(self) -> float:
        return np.sum(self._pnl)

    @property
    def total_fee(self) -> float:
        return np.sum(self._fee)

    @property
    def average_pnl(self) -> float:
        if self.total_trades < TOTAL_TRADES_THRESHOLD:
            return 0

        return np.mean(self._pnl)

    @property
    def average_win(self) -> float:
        win = self._pnl[self._pnl > 0]

        if len(win) < 2:
            return 0

        return np.mean(win)

    @property
    def average_loss(self) -> float:
        loss = self._pnl[self._pnl < 0]

        if len(loss) < 2:
            return 0

        return np.mean(loss)

    @property
    def max_consecutive_wins(self) -> int:
        return self._max_streak(self._pnl, True)

    @property
    def max_consecutive_losses(self) -> int:
        return self._max_streak(self._pnl, False)

    @property
    def hit_ratio(self) -> float:
        total_trades = self.total_trades

        if total_trades < TOTAL_TRADES_THRESHOLD:
            return 0

        return np.sum(self._pnl > 0) / total_trades

    @property
    def equity(self):
        return [self._account_size] + self._pnl.cumsum()

    @property
    def drawdown(self):
        equity_curve = self.equity

        if len(equity_curve) < 2:
            return np.array([0, 0])

        peak = np.maximum.accumulate(equity_curve)
        drawdowns = (peak - equity_curve) / peak

        return drawdowns

    @property
    def runup(self) -> float:
        equity_curve = self.equity

        if len(equity_curve) < 2:
            return np.array([0, 0])

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

        return self.cagr / np.abs(max_drawdown)

    @property
    def sharpe_ratio(self) -> float:
        if self.total_trades < TOTAL_TRADES_THRESHOLD:
            return 0

        std_return = np.std(self._pnl, ddof=1)

        if std_return == 0:
            return 0

        return self.average_pnl / std_return

    @property
    def smart_sharpe_ratio(self) -> float:
        if self.total_trades < TOTAL_TRADES_THRESHOLD:
            return 0

        std_return = np.std(self._pnl, ddof=1)
        penalty = self._penalty(self._pnl)

        if std_return == 0 or penalty == 0:
            return 0

        return self.average_pnl / std_return * penalty

    @property
    def deflated_sharpe_ratio(self) -> float:
        total_trades = self.total_trades

        if total_trades < TOTAL_TRADES_THRESHOLD:
            return 0

        sharpe_ratio = self.sharpe_ratio
        skewness = self.skew
        kurtosis = self.kurtosis

        gamma = 0.57721566
        e = np.exp(1)

        sharpe_ratio_star = np.sqrt(0.5 / self._periods_per_year) * (
            (1 - gamma) * norm.ppf(1 - 1 / total_trades)
            + gamma * norm.ppf(1 - 1 / (total_trades * e))
        )

        denom = 1 - skewness * sharpe_ratio + ((kurtosis - 1) / 4) * sharpe_ratio**2

        if denom <= 0:
            return 0

        return norm.cdf(
            ((sharpe_ratio - sharpe_ratio_star) * np.sqrt(total_trades - 1))
            / np.sqrt(denom)
        )

    @property
    def sortino_ratio(self) -> float:
        total_trades = self.total_trades

        if total_trades < TOTAL_TRADES_THRESHOLD:
            return 0

        downside_returns = self._pnl[self._pnl < 0]

        if len(downside_returns) < 2:
            return 0

        downside = np.sqrt(np.sum(downside_returns**2) / total_trades)

        if downside == 0:
            return 0

        return self.average_pnl / downside

    @property
    def smart_sortino_ratio(self) -> float:
        total_trades = self.total_trades

        if total_trades < TOTAL_TRADES_THRESHOLD:
            return 0

        downside_returns = self._pnl[self._pnl < 0]

        if len(downside_returns) < 2:
            return 0

        downside = np.sqrt(np.sum(downside_returns**2) / total_trades)
        penalty = self._penalty(self._pnl)

        if downside == 0 or penalty == 0:
            return 0

        return self.average_pnl / downside * penalty

    @property
    def payoff_ratio(self) -> float:
        if self.total_trades < TOTAL_TRADES_THRESHOLD:
            return 0

        denom = abs(self.average_loss)

        if denom == 0:
            return 0

        return self.average_win / denom

    @property
    def cagr(self) -> float:
        periods = self.total_trades

        if periods < TOTAL_TRADES_THRESHOLD:
            return 0

        equity = self.equity

        if len(equity) < 2:
            return 0

        final_value = equity[-1]
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
        total_trades = self.total_trades

        if total_trades < TOTAL_TRADES_THRESHOLD:
            return self._risk_per_trade

        equity = self.equity

        max_loss = np.abs(np.min(self._pnl))
        initial_value = self._account_size
        growth_factor = equity[-1] / initial_value

        if growth_factor <= 0:
            return self._risk_per_trade

        return (max_loss / np.abs(initial_value)) * np.sqrt(growth_factor)

    @property
    def kelly(self) -> float:
        total_trades = self.total_trades

        if total_trades < TOTAL_TRADES_THRESHOLD:
            return self._risk_per_trade

        wl_ratio = self.payoff_ratio

        if wl_ratio == 0:
            return self._risk_per_trade

        win_prob = self.hit_ratio

        return win_prob - ((1 - win_prob) / wl_ratio)

    @property
    def ann_sharpe_ratio(self) -> float:
        return self.sharpe_ratio * np.sqrt(self._periods_per_year)

    @property
    def expected_return(self) -> float:
        total_trades = self.total_trades

        if total_trades < TOTAL_TRADES_THRESHOLD:
            return 0

        prod = np.prod(1 + self._pnl)

        if prod <= 0:
            return 0

        return prod ** (1 / total_trades) - 1

    @property
    def ann_volatility(self) -> float:
        if self.total_trades < TOTAL_TRADES_THRESHOLD:
            return 0

        daily_returns = self._pnl / self._account_size
        volatility = np.std(daily_returns, ddof=1)

        return volatility * np.sqrt(self._periods_per_year)

    @property
    def recovery_factor(self) -> float:
        max_drawdown = self.max_drawdown

        if max_drawdown == 0:
            return 0

        total_profit = np.sum(self._pnl[self._pnl > 0])

        return total_profit / max_drawdown

    @property
    def profit_factor(self) -> float:
        if self.total_trades < TOTAL_TRADES_THRESHOLD:
            return 0

        pnl_positive = self._pnl > 0
        gross_profit = np.sum(self._pnl[pnl_positive])
        gross_loss = np.abs(np.sum(self._pnl[~pnl_positive]))

        if gross_loss == 0:
            return 0

        return gross_profit / gross_loss

    @property
    def risk_of_ruin(self) -> float:
        total_trades = self.total_trades

        if total_trades < TOTAL_TRADES_THRESHOLD:
            return 0

        win_rate = self.hit_ratio

        return ((1 - win_rate) / (1 + win_rate)) ** total_trades

    @property
    def skew(self) -> float:
        total_trades = self.total_trades

        if total_trades < TOTAL_TRADES_THRESHOLD:
            return 0

        return skew(self._pnl, bias=False)

    @property
    def kurtosis(self) -> float:
        total_trades = self.total_trades

        if total_trades < TOTAL_TRADES_THRESHOLD:
            return 0

        return kurtosis(self._pnl, bias=False)

    @property
    def var(self, confidence_level=0.95) -> float:
        if self.total_trades < TOTAL_TRADES_THRESHOLD:
            return 0

        mu = self.average_pnl
        sigma = np.std(self._pnl, ddof=1)

        return norm.ppf(1 - confidence_level, mu, sigma)

    @property
    def cvar(self) -> float:
        if self.total_trades < TOTAL_TRADES_THRESHOLD:
            return 0

        var = self.var
        pnl = self._pnl[self._pnl < var]

        if len(pnl) < 2:
            return var

        return np.mean(pnl)

    @property
    def ulcer_index(self) -> float:
        if self.total_trades < TOTAL_TRADES_THRESHOLD:
            return 0

        drawdown = self.drawdown

        if len(drawdown) < 2:
            return 0

        return np.sqrt(np.mean(drawdown**2)) * 100

    @property
    def upi(self) -> float:
        ulcer_index = self.ulcer_index

        if ulcer_index == 0:
            return 0

        prod = np.prod(1 + self._pnl) - 1

        return prod / ulcer_index

    @property
    def common_sense_ratio(self) -> float:
        if self.total_trades < TOTAL_TRADES_THRESHOLD:
            return 0

        return self.profit_factor * self.tail_ratio

    @property
    def cpc_ratio(self) -> float:
        if self.total_trades < TOTAL_TRADES_THRESHOLD:
            return 0

        return self.profit_factor * self.hit_ratio * self.payoff_ratio

    @property
    def lake_ratio(self) -> float:
        if self.total_trades < TOTAL_TRADES_THRESHOLD:
            return 0

        equity = self.equity

        if len(equity) < 2:
            return 0

        peaks = np.maximum.accumulate(equity)
        drawdowns = (peaks - equity) / peaks
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

        if len(shortfall) < 2:
            return 0

        expected_shortfall = np.abs(np.mean(shortfall))

        if expected_shortfall == 0:
            return 0

        return np.abs(self.average_pnl) / expected_shortfall

    @property
    def sterling_ratio(self) -> float:
        if self.total_trades < TOTAL_TRADES_THRESHOLD:
            return 0

        gains, losses = self._pnl[self._pnl > 0], self._pnl[self._pnl < 0]

        if len(losses) < 2 or len(gains) < 2:
            return 0

        upside_potential = np.mean(gains)
        downside_risk = np.sqrt(np.mean(losses**2))

        if downside_risk == 0:
            return 0

        return upside_potential / downside_risk

    @property
    def tail_ratio(self, cutoff=95) -> float:
        if self.total_trades < TOTAL_TRADES_THRESHOLD:
            return 0

        return abs(
            np.percentile(self._pnl, cutoff) / np.percentile(self._pnl, 100 - cutoff)
        )

    @property
    def omega_ratio(self) -> float:
        if self.total_trades < TOTAL_TRADES_THRESHOLD:
            return 0

        gains, losses = self._pnl[self._pnl > 0], self._pnl[self._pnl < 0]

        if len(losses) == 0 or len(gains) == 0:
            return 0

        sum_losses = np.sum(np.abs(losses))

        if sum_losses == 0:
            return 0

        return np.sum(gains) / sum_losses

    @property
    def kappa_three_ratio(self) -> float:
        if self.total_trades < TOTAL_TRADES_THRESHOLD:
            return 0

        gains, losses = self._pnl[self._pnl > 0], self._pnl[self._pnl < 0]

        if len(losses) < 2 or len(gains) < 2:
            return 0

        avg_gain, avg_loss = np.mean(gains), np.mean(losses)

        threshold = avg_gain - avg_loss

        up_proportion = np.sum(gains > threshold) / self.total_trades
        down_proportion = np.sum(losses < threshold) / self.total_trades

        return (up_proportion**3 - down_proportion) / np.sqrt(np.mean(self._pnl**2))

    def next(self, pnl: float, fee: float) -> "Performance":
        _pnl, _fee = np.append(self._pnl, pnl), np.append(self._fee, fee)

        return replace(self, _pnl=_pnl, _fee=_fee)

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
    def _penalty(pnl) -> float:
        if len(pnl) < TOTAL_TRADES_THRESHOLD:
            return 1

        coef = np.abs(np.corrcoef(pnl[:-1], pnl[1:])[0, 1])
        num = len(pnl)
        corr = [((num - x) / num) * coef**x for x in range(1, num)]

        return np.sqrt(1 + 2 * np.sum(corr))

    def __repr__(self):
        return (
            f"Performance(total_trades={self.total_trades}, hit_ratio={self.hit_ratio}, profit_factor={self.profit_factor}, "
            + f"max_runup={self.max_runup}, max_drawdown={self.max_drawdown}, sortino_ratio={self.sortino_ratio}, smart_sortino_ratio={self.smart_sortino_ratio}, calmar_ratio={self.calmar_ratio}, "
            + f"risk_of_ruin={self.risk_of_ruin}, recovery_factor={self.recovery_factor}, optimal_f={self.optimal_f}, "
            + f"total_pnl={self.total_pnl}, average_pnl={self.average_pnl}, total_fee={self.total_fee}, sharpe_ratio={self.sharpe_ratio}, smart_sharpe_ratio={self.smart_sharpe_ratio}, deflated_sharpe_ratio={self.deflated_sharpe_ratio}, "
            + f"max_consecutive_wins={self.max_consecutive_wins}, max_consecutive_losses={self.max_consecutive_losses}, average_win={self.average_win}, average_loss={self.average_loss}, "
            + f"cagr={self.cagr}, expected_return={self.expected_return}, annualized_volatility={self.ann_volatility}, annualized_sharpe_ratio={self.ann_sharpe_ratio}, payoff_ratio={self.payoff_ratio}, "
            + f"var={self.var}, cvar={self.cvar}, ulcer_index={self.ulcer_index}, upi={self.upi}, kelly={self.kelly}, "
            + f"lake_ratio={self.lake_ratio}, burke_ratio={self.burke_ratio}, rachev_ratio={self.rachev_ratio}, kappa_three_ratio={self.kappa_three_ratio}, "
            + f"sterling_ratio={self.sterling_ratio}, tail_ratio={self.tail_ratio}, omega_ratio={self.omega_ratio}, cpc_ratio={self.cpc_ratio}, common_sense_ratio={self.common_sense_ratio}, "
            + f"skew={self.skew}, kurtosis={self.kurtosis})"
        )

    def to_dict(self):
        return {
            "account_size": self._account_size,
            "total_trades": self.total_trades,
            "total_pnl": self.total_pnl,
            "total_fee": self.total_fee,
            "average_pnl": self.average_pnl,
            "average_win": self.average_win,
            "average_loss": self.average_loss,
            "max_consecutive_wins": self.max_consecutive_wins,
            "max_consecutive_losses": self.max_consecutive_losses,
            "hit_ratio": self.hit_ratio,
            "equity": self.equity,
            "runup": self.runup,
            "max_runup": self.max_runup,
            "drawdown": self.drawdown,
            "max_drawdown": self.max_drawdown,
            "sharpe_ratio": self.sharpe_ratio,
            "smart_sharpe_ratio": self.smart_sharpe_ratio,
            "deflated_sharpe_ratio": self.deflated_sharpe_ratio,
            "calmar_ratio": self.calmar_ratio,
            "cpc_ratio": self.cpc_ratio,
            "common_sense_ratio": self.common_sense_ratio,
            "sortino_ratio": self.sortino_ratio,
            "smart_sortino_ratio": self.smart_sortino_ratio,
            "payoff_ratio": self.payoff_ratio,
            "cagr": self.cagr,
            "optimal_f": self.optimal_f,
            "kelly": self.kelly,
            "expected_return": self.expected_return,
            "annualized_volatility": self.ann_volatility,
            "annualized_sharpe_ratio": self.ann_sharpe_ratio,
            "recovery_factor": self.recovery_factor,
            "profit_factor": self.profit_factor,
            "risk_of_ruin": self.risk_of_ruin,
            "skew": self.skew,
            "kurtosis": self.kurtosis,
            "var": self.var,
            "cvar": self.cvar,
            "ulcer_index": self.ulcer_index,
            "upi": self.upi,
            "lake_ratio": self.lake_ratio,
            "burke_ratio": self.burke_ratio,
            "rachev_ratio": self.rachev_ratio,
            "sterling_ratio": self.sterling_ratio,
            "tail_ratio": self.tail_ratio,
            "omega_ratio": self.omega_ratio,
            "kappa_three_ratio": self.kappa_three_ratio,
        }
