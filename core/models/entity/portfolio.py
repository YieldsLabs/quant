from dataclasses import field, replace
from datetime import datetime
from functools import cached_property

import numpy as np
from scipy.stats import kurtosis, norm, skew

from ._base import Entity

TOTAL_TRADES_THRESHOLD = 3
GAMMA = 0.57721566


@Entity
class Performance:
    _account_size: float
    _risk_per_trade: float
    _periods_per_year: float = 252
    _pnl: np.array = field(default_factory=lambda: np.array([], dtype=np.float64))
    _fee: np.array = field(default_factory=lambda: np.array([], dtype=np.float64))
    updated_at: float = field(default_factory=lambda: datetime.now().timestamp())

    @property
    def equity(self):
        return np.array([self._account_size]) + np.cumsum(self._pnl)

    @cached_property
    def total_trades(self) -> int:
        return len(self._pnl)

    @cached_property
    def total_pnl(self) -> float:
        return np.sum(self._pnl)

    @cached_property
    def average_pnl(self) -> float:
        if self.total_trades < TOTAL_TRADES_THRESHOLD:
            return 0.0

        if len(self._pnl) < 2:
            return 0.0

        return np.mean(self._pnl)

    @property
    def profit(self):
        if self.total_trades < TOTAL_TRADES_THRESHOLD:
            return np.array([0.0])

        return self._pnl[self._pnl > 0]

    @property
    def loss(self):
        if self.total_trades < TOTAL_TRADES_THRESHOLD:
            return np.array([0.0])

        return self._pnl[self._pnl < 0]

    @cached_property
    def total_profit(self):
        return np.sum(self.profit)

    @cached_property
    def total_loss(self):
        return np.sum(self.loss)

    @cached_property
    def total_fee(self) -> float:
        return np.sum(self._fee)

    @cached_property
    def hit_ratio(self) -> float:
        if self.total_trades < TOTAL_TRADES_THRESHOLD:
            return 0.0

        return np.sum(self._pnl > 0) / self.total_trades

    @cached_property
    def average_profit(self) -> float:
        if len(self.profit) < 2:
            return 0.0

        return np.mean(self.profit)

    @cached_property
    def average_loss(self) -> float:
        if len(self.loss) < 2:
            return 0.0

        return np.mean(self.loss)

    @cached_property
    def max_consecutive_wins(self) -> int:
        return self._max_streak(self._pnl, True)

    @cached_property
    def max_consecutive_losses(self) -> int:
        return self._max_streak(self._pnl, False)

    @property
    def drawdown(self):
        if self.total_trades < TOTAL_TRADES_THRESHOLD:
            return np.array([0.0])

        peak = np.maximum.accumulate(self.equity)
        return (peak - self.equity) / peak

    @property
    def runup(self):
        if self.total_trades < TOTAL_TRADES_THRESHOLD:
            return np.array([0.0])

        trough = np.minimum.accumulate(self.equity)
        return (self.equity - trough) / trough

    @cached_property
    def max_runup(self) -> float:
        if len(self.runup) == 0:
            return 0.0

        return np.max(self.runup)

    @cached_property
    def max_drawdown(self) -> float:
        if len(self.drawdown) == 0:
            return 0.0

        return np.max(self.drawdown)

    @cached_property
    def calmar_ratio(self) -> float:
        denom = abs(self.max_drawdown)

        if denom == 0:
            return 0.0

        return self.cagr / denom

    @cached_property
    def sharpe_ratio(self) -> float:
        if self.total_trades < TOTAL_TRADES_THRESHOLD:
            return 0.0

        std_return = np.std(self._pnl, ddof=1)
        if std_return == 0:
            return 0.0

        return self.average_pnl / std_return

    @cached_property
    def smart_sharpe_ratio(self) -> float:
        if self.total_trades < TOTAL_TRADES_THRESHOLD:
            return 0

        std_return = np.std(self._pnl, ddof=1)
        penalty = self._penalty(self._pnl)

        denom = std_return * penalty

        if denom == 0:
            return 0.0

        return self.average_pnl / denom

    @cached_property
    def deflated_sharpe_ratio(self) -> float:
        if self.total_trades < TOTAL_TRADES_THRESHOLD:
            return 0

        e = np.exp(1)

        sharpe_ratio_star = np.sqrt(0.5 / self._periods_per_year) * (
            (1 - GAMMA) * norm.ppf(1 - 1 / self.total_trades)
            + GAMMA * norm.ppf(1 - 1 / (self.total_trades * e))
        )

        denom = (
            1
            - self.skew * self.sharpe_ratio
            + ((self.kurtosis - 1) / 4) * self.sharpe_ratio**2
        )

        if denom <= 0:
            return 0

        return norm.cdf(
            (self.sharpe_ratio - sharpe_ratio_star)
            * np.sqrt(self.total_trades - 1)
            / np.sqrt(denom)
        )

    @cached_property
    def sortino_ratio(self) -> float:
        if self.total_trades < TOTAL_TRADES_THRESHOLD:
            return 0.0

        downside = np.sqrt(np.sum(self.loss**2) / self.total_trades)

        if downside == 0:
            return 0.0

        return self.average_pnl / downside

    @cached_property
    def smart_sortino_ratio(self) -> float:
        if self.total_trades < TOTAL_TRADES_THRESHOLD:
            return 0.0

        downside = np.sqrt(np.sum(self.loss**2) / self.total_trades)
        penalty = self._penalty(self._pnl)

        denom = downside * penalty

        if denom == 0:
            return 0.0

        return self.average_pnl / denom

    @cached_property
    def payoff_ratio(self) -> float:
        if self.total_trades < TOTAL_TRADES_THRESHOLD:
            return 0.0

        denom = abs(self.average_loss)

        if denom == 0:
            return 0.0

        return self.average_profit / denom

    @cached_property
    def cagr(self) -> float:
        if self.total_trades < TOTAL_TRADES_THRESHOLD:
            return 0.0

        final_value = self.equity[-1]
        initial_value = self._account_size

        if initial_value == 0:
            return 0.0
        if final_value < initial_value:
            return -1.0

        compound_factor = final_value / initial_value
        time_factor = 1 / (self.total_trades / self._periods_per_year)

        return np.power(compound_factor, time_factor) - 1

    @cached_property
    def kelly(self) -> float:
        if self.total_trades < TOTAL_TRADES_THRESHOLD:
            return self._risk_per_trade

        if self.payoff_ratio == 0:
            return self._risk_per_trade

        return self.hit_ratio - (1 - self.hit_ratio) / self.payoff_ratio

    @cached_property
    def ann_sharpe_ratio(self) -> float:
        return self.sharpe_ratio * np.sqrt(self._periods_per_year)

    @cached_property
    def time_weighted_return(self) -> float:
        if self.total_trades < TOTAL_TRADES_THRESHOLD:
            return 0.0

        if len(self.equity) < 2:
            return 0.0

        return (self.equity[-1] / self.equity[0]) - 1

    @cached_property
    def geometric_holding_period_return(self) -> float:
        if self.total_trades < TOTAL_TRADES_THRESHOLD:
            return 0.0

        return (1 + self.time_weighted_return) ** (1 / self.total_trades) - 1

    @cached_property
    def expected_return(self) -> float:
        if self.total_trades < TOTAL_TRADES_THRESHOLD:
            return 0.0

        log_prod = np.sum(np.log(1.0 + self.profit))

        if log_prod <= 0:
            return 0.0

        return np.exp(log_prod / self.total_trades) - 1.0

    @cached_property
    def ann_volatility(self) -> float:
        if self.total_trades < TOTAL_TRADES_THRESHOLD:
            return 0.0

        daily_returns = self._pnl / self._account_size

        volatility = np.std(daily_returns, ddof=1)

        return volatility * np.sqrt(self._periods_per_year)

    @cached_property
    def recovery_factor(self) -> float:
        if self.max_drawdown == 0:
            return 0.0

        return self.total_profit / self.max_drawdown

    @cached_property
    def profit_factor(self) -> float:
        if self.total_trades < TOTAL_TRADES_THRESHOLD:
            return 0.0

        gross_loss = abs(self.total_loss)

        if gross_loss == 0:
            return 0.0

        return self.total_profit / gross_loss

    @cached_property
    def risk_of_ruin(self) -> float:
        if self.total_trades < TOTAL_TRADES_THRESHOLD:
            return 0.0

        return ((1 - self.hit_ratio) / (1 + self.hit_ratio)) ** self.total_trades

    @cached_property
    def skew(self) -> float:
        if self.total_trades < TOTAL_TRADES_THRESHOLD:
            return 0.0

        return skew(self._pnl, bias=False)

    @cached_property
    def kurtosis(self) -> float:
        if self.total_trades < TOTAL_TRADES_THRESHOLD:
            return 0.0

        return kurtosis(self._pnl, bias=False)

    @cached_property
    def var(self, confidence_level=0.95) -> float:
        if self.total_trades < TOTAL_TRADES_THRESHOLD:
            return 0.0

        mu = self.average_pnl
        sigma = np.std(self._pnl, ddof=1)

        return norm.ppf(1.0 - confidence_level, mu, sigma)

    @cached_property
    def cvar(self) -> float:
        if self.total_trades < TOTAL_TRADES_THRESHOLD:
            return 0.0

        var = self.var
        pnl = self._pnl[self._pnl < var]

        if len(pnl) < 2:
            return var

        return np.mean(pnl)

    @cached_property
    def ulcer_index(self) -> float:
        if self.total_trades < TOTAL_TRADES_THRESHOLD:
            return 0.0

        if len(self.drawdown) < 2:
            return 0.0

        return np.sqrt(np.mean(self.drawdown**2))

    @cached_property
    def upi(self) -> float:
        if self.ulcer_index == 0:
            return 0.0

        return self.expected_return / self.ulcer_index

    @cached_property
    def common_sense_ratio(self) -> float:
        if self.total_trades < TOTAL_TRADES_THRESHOLD:
            return 0.0

        return self.profit_factor * self.tail_ratio

    @cached_property
    def cpc_ratio(self) -> float:
        if self.total_trades < TOTAL_TRADES_THRESHOLD:
            return 0.0

        return self.profit_factor * self.hit_ratio * self.payoff_ratio

    @cached_property
    def lake_ratio(self) -> float:
        if self.total_trades < TOTAL_TRADES_THRESHOLD:
            return 0.0

        underwater_time = np.sum(self.drawdown < 0) / self._periods_per_year

        return 1 - underwater_time

    @cached_property
    def burke_ratio(self) -> float:
        if self.total_trades < TOTAL_TRADES_THRESHOLD:
            return 0.0

        downside_deviation = np.std(np.minimum(self._pnl, 0), ddof=1)

        if downside_deviation == 0:
            return 0.0

        return self.cagr / downside_deviation

    @cached_property
    def rachev_ratio(self) -> float:
        if self.total_trades < TOTAL_TRADES_THRESHOLD:
            return 0.0

        pnl_sorted = np.sort(self._pnl)[::-1]
        var_95 = np.percentile(pnl_sorted, 5)

        shortfall = pnl_sorted[pnl_sorted <= var_95]
        if len(shortfall) < 2:
            return 0.0

        expected_shortfall = np.abs(np.mean(shortfall))
        if expected_shortfall == 0:
            return 0.0

        return abs(self.average_pnl) / expected_shortfall

    @cached_property
    def sterling_ratio(self) -> float:
        if self.total_trades < TOTAL_TRADES_THRESHOLD:
            return 0.0

        if len(self.loss) < 2:
            return 0.0

        downside_risk = np.sqrt(np.mean(self.loss**2))

        if downside_risk == 0:
            return 0.0

        return self.average_profit / downside_risk

    @cached_property
    def tail_ratio(self, cutoff=95) -> float:
        if self.total_trades < TOTAL_TRADES_THRESHOLD:
            return 0.0

        denom = np.percentile(self._pnl, 100 - cutoff)
        if denom == 0:
            return 0.0

        return abs(np.percentile(self._pnl, cutoff) / denom)

    @cached_property
    def omega_ratio(self) -> float:
        if self.total_trades < TOTAL_TRADES_THRESHOLD:
            return 0.0

        gross_loss = abs(self.total_loss)

        if gross_loss == 0:
            return 0.0

        return self.total_profit / gross_loss

    @cached_property
    def martin_ratio(self) -> float:
        if self.ulcer_index == 0:
            return 0.0

        return self.average_pnl / self.ulcer_index

    @cached_property
    def kappa_three_ratio(self) -> float:
        if self.total_trades < TOTAL_TRADES_THRESHOLD:
            return 0.0

        threshold = self.average_profit - self.average_loss

        if threshold == 0:
            return 0.0

        up_proportion = np.sum(self.profit > threshold) / self.total_trades
        down_proportion = np.sum(self.loss < threshold) / self.total_trades

        if len(self._pnl) < 2:
            return 0.0

        denom = np.sqrt(np.mean(self._pnl**2))

        if denom == 0:
            return 0.0

        return (up_proportion**3 - down_proportion) / denom

    def next(self, pnl: float, fee: float) -> "Performance":
        _pnl, _fee = np.append(self._pnl, pnl), np.append(self._fee, fee)

        return replace(
            self, _pnl=_pnl, _fee=_fee, updated_at=datetime.now().timestamp()
        )

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

        x = pnl[:-1]
        y = pnl[1:]
        y[0] += 1e-15
        coef = np.abs(np.corrcoef(x, y)[0, 1])
        num = len(pnl)
        corr = [((num - x) / num) * coef**x for x in range(1, num)]

        return np.sqrt(1 + 2 * np.sum(corr))
