from dataclasses import field, replace
from datetime import datetime
from functools import cached_property

import numpy as np
from scipy.stats import kurtosis, norm, skew

from ._base import Entity

TOTAL_TRADES_THRESHOLD = 3
SMALL_NUMBER_THRESHOLD = np.finfo(float).eps
GAMMA = 0.57721566


@Entity
class Performance:
    _account_size: float
    _risk_per_trade: float
    _periods_per_year: float = 252
    _mar: float = 0.0
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

        return np.mean(self._pnl) if len(self._pnl) >= 2 else 0.0

    @property
    def profit(self):
        if self.total_trades < TOTAL_TRADES_THRESHOLD:
            return np.zeros_like(self.equity)

        return self._pnl[self._pnl > 0]

    @property
    def loss(self):
        if self.total_trades < TOTAL_TRADES_THRESHOLD:
            return np.zeros_like(self.equity)

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
        return np.mean(self.profit) if len(self.profit) >= 2 else 0.0

    @cached_property
    def average_loss(self) -> float:
        return np.mean(self.loss) if len(self.loss) >= 2 else 0.0

    @cached_property
    def max_consecutive_wins(self) -> int:
        return self._max_streak(self._pnl, True)

    @cached_property
    def max_consecutive_losses(self) -> int:
        return self._max_streak(self._pnl, False)

    @property
    def drawdown(self):
        if self.total_trades < TOTAL_TRADES_THRESHOLD:
            return np.zeros_like(self.equity)

        peak = np.maximum.accumulate(self.equity)
        drawdown = np.where(peak > 0, (peak - self.equity) / peak, 0.0)

        return drawdown

    @property
    def runup(self):
        if self.total_trades < TOTAL_TRADES_THRESHOLD:
            return np.zeros_like(self.equity)

        trough = np.minimum.accumulate(self.equity)
        runup = np.where(trough > 0, (self.equity - trough) / trough, 0.0)

        return runup

    @cached_property
    def max_runup(self) -> float:
        return np.max(self.runup) if len(self.runup) >= 2 else 0.0

    @cached_property
    def max_drawdown(self) -> float:
        return np.max(self.drawdown) if len(self.drawdown) >= 2 else 0.0

    @cached_property
    def cagr(self) -> float:
        if self.total_trades < TOTAL_TRADES_THRESHOLD:
            return 0.0

        final_value = self.equity[-1]
        initial_value = self._account_size

        if initial_value == 0:
            return 0.0

        if final_value == 0:
            return -1.0

        compound_factor = final_value / initial_value
        time_factor = 1 / max(self.total_trades / self._periods_per_year, 1)

        return np.power(compound_factor, time_factor) - 1

    @cached_property
    def daily_returns(self) -> np.array:
        if self.total_trades < TOTAL_TRADES_THRESHOLD:
            return np.zeros_like(self._pnl)

        return self._pnl / self._account_size

    @cached_property
    def average_daily_return(self) -> float:
        return np.mean(self.daily_returns) if len(self.daily_returns) >= 2 else 0.0

    @cached_property
    def time_weighted_return(self) -> float:
        if self.total_trades < TOTAL_TRADES_THRESHOLD:
            return 0.0

        if len(self.equity) < 2:
            return 0.0

        initial_equity = self.equity[0]

        if initial_equity == 0:
            return 0.0

        return (self.equity[-1] / initial_equity) - 1

    @cached_property
    def geometric_holding_period_return(self) -> float:
        if self.total_trades < TOTAL_TRADES_THRESHOLD:
            return 0.0

        if self.time_weighted_return <= -1.0:
            return 0.0

        return (1 + self.time_weighted_return) ** (1 / self.total_trades) - 1

    @cached_property
    def expected_return(self) -> float:
        if self.total_trades < TOTAL_TRADES_THRESHOLD:
            return 0.0

        if np.any(self.profit < -1.0):
            return 0.0

        log_prod = np.sum(np.log(1.0 + self.profit))

        return (
            np.exp(log_prod / self.total_trades) - 1.0
            if log_prod > SMALL_NUMBER_THRESHOLD
            else 0.0
        )

    @cached_property
    def excess_return(self) -> float:
        return self.average_pnl - self._mar

    @cached_property
    def daily_volatility(self) -> float:
        return (
            np.std(self.daily_returns, ddof=1) if len(self.daily_returns) >= 2 else 0.0
        )

    @cached_property
    def ann_volatility(self) -> float:
        if self.total_trades < TOTAL_TRADES_THRESHOLD:
            return 0.0

        return self.daily_volatility * np.sqrt(self._periods_per_year)

    @cached_property
    def information_ratio(self) -> float:
        if self.total_trades < TOTAL_TRADES_THRESHOLD:
            return 0.0

        return (
            self.average_daily_return / self.ann_volatility
            if self.ann_volatility > SMALL_NUMBER_THRESHOLD
            else 0.0
        )

    @cached_property
    def calmar_ratio(self) -> float:
        denom = abs(self.max_drawdown)

        return self.cagr / denom if denom > SMALL_NUMBER_THRESHOLD else 0.0

    @cached_property
    def sharpe_ratio(self) -> float:
        if self.total_trades < TOTAL_TRADES_THRESHOLD:
            return 0.0

        std_return = np.std(self._pnl, ddof=1)

        return (
            self.average_pnl / std_return
            if std_return > SMALL_NUMBER_THRESHOLD
            else 0.0
        )

    @cached_property
    def smart_sharpe_ratio(self) -> float:
        if self.total_trades < TOTAL_TRADES_THRESHOLD:
            return 0.0

        std_return = np.std(self._pnl, ddof=1)
        penalty = self._penalty(self._pnl)

        denom = std_return * penalty

        return self.average_pnl / denom if denom > SMALL_NUMBER_THRESHOLD else 0.0

    @cached_property
    def deflated_sharpe_ratio(self) -> float:
        if self.total_trades < TOTAL_TRADES_THRESHOLD:
            return 0.0

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

        return (
            norm.cdf(
                (self.sharpe_ratio - sharpe_ratio_star)
                * np.sqrt(self.total_trades - 1)
                / np.sqrt(denom)
            )
            if denom > SMALL_NUMBER_THRESHOLD
            else 0.0
        )

    @cached_property
    def sortino_ratio(self) -> float:
        if self.total_trades < TOTAL_TRADES_THRESHOLD:
            return 0.0

        downside_risk = np.sqrt(self._lpm(order=2))

        return (
            self.excess_return / downside_risk
            if downside_risk > SMALL_NUMBER_THRESHOLD
            else 0.0
        )

    @cached_property
    def omega_ratio(self) -> float:
        if self.total_trades < TOTAL_TRADES_THRESHOLD:
            return 0.0

        downside_risk = self._lpm(order=1)

        return (
            (self.excess_return / downside_risk) + 1.0
            if downside_risk > SMALL_NUMBER_THRESHOLD
            else 0.0
        )

    @cached_property
    def kappa_three_ratio(self) -> float:
        if self.total_trades < TOTAL_TRADES_THRESHOLD:
            return 0.0

        downside_risk = np.cbrt(self._lpm(order=3))

        return (
            self.excess_return / downside_risk
            if downside_risk > SMALL_NUMBER_THRESHOLD
            else 0.0
        )

    @cached_property
    def payoff_ratio(self) -> float:
        if self.total_trades < TOTAL_TRADES_THRESHOLD:
            return 0.0

        denom = abs(self.average_loss)

        return self.average_profit / denom if denom > SMALL_NUMBER_THRESHOLD else 0.0

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
    def recovery_factor(self) -> float:
        return (
            self.total_profit / self.max_drawdown
            if self.max_drawdown > SMALL_NUMBER_THRESHOLD
            else 0.0
        )

    @cached_property
    def profit_factor(self) -> float:
        if self.total_trades < TOTAL_TRADES_THRESHOLD:
            return 0.0

        gross_loss = abs(self.total_loss)

        return (
            self.total_profit / gross_loss
            if gross_loss > SMALL_NUMBER_THRESHOLD
            else 0.0
        )

    @cached_property
    def risk_of_ruin(self) -> float:
        if self.total_trades < TOTAL_TRADES_THRESHOLD:
            return 0.0

        if self.hit_ratio == 0:
            return 1.0

        if self.hit_ratio == 1:
            return 0.0

        return ((1 - self.hit_ratio) / (1 + self.hit_ratio)) ** self.total_trades

    @cached_property
    def common_sense_ratio(self) -> float:
        if self.total_trades < TOTAL_TRADES_THRESHOLD:
            return 0.0

        if (
            self.profit_factor < SMALL_NUMBER_THRESHOLD
            or self.tail_ratio < SMALL_NUMBER_THRESHOLD
        ):
            return 0.0

        return self.profit_factor * self.tail_ratio

    @cached_property
    def cpc_ratio(self) -> float:
        if self.total_trades < TOTAL_TRADES_THRESHOLD:
            return 0.0

        return self.profit_factor * self.hit_ratio * self.payoff_ratio

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

        pnl_sorted = np.sort(self._pnl)
        var_index = int((1.0 - confidence_level) * self.total_trades)

        return pnl_sorted[var_index]

    @cached_property
    def cvar(self) -> float:
        if self.total_trades < TOTAL_TRADES_THRESHOLD:
            return 0.0

        pnl = self._pnl[self._pnl < self.var]

        return np.mean(pnl) if len(pnl) >= 2 else self.var

    @cached_property
    def ulcer_index(self) -> float:
        if self.total_trades < TOTAL_TRADES_THRESHOLD:
            return 0.0

        return np.sqrt(np.mean(self.drawdown**2)) if len(self.drawdown) >= 2 else 0.0

    @cached_property
    def upi(self) -> float:
        return (
            self.expected_return / self.ulcer_index
            if self.ulcer_index > SMALL_NUMBER_THRESHOLD
            else 0.0
        )

    @cached_property
    def martin_ratio(self) -> float:
        return (
            self.average_pnl / self.ulcer_index
            if self.ulcer_index > SMALL_NUMBER_THRESHOLD
            else 0.0
        )

    @cached_property
    def lake_ratio(self) -> float:
        if self.total_trades < TOTAL_TRADES_THRESHOLD:
            return 0.0

        return (
            1 - np.sum(self.drawdown < 0) / self._periods_per_year
            if len(self.drawdown) >= 2
            else 0.0
        )

    @cached_property
    def burke_ratio(self) -> float:
        if self.total_trades < TOTAL_TRADES_THRESHOLD:
            return 0.0

        downside_deviation = np.std(np.minimum(self._pnl, 0), ddof=1)

        return (
            self.cagr / downside_deviation
            if downside_deviation > SMALL_NUMBER_THRESHOLD
            else 0.0
        )

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

        if expected_shortfall < SMALL_NUMBER_THRESHOLD:
            return 0.0

        var_5 = np.percentile(pnl_sorted, 95)
        upside = pnl_sorted[pnl_sorted >= var_5]

        if len(upside) < 2:
            return 0.0

        expected_upside = np.mean(upside)

        if expected_upside < SMALL_NUMBER_THRESHOLD:
            return 0.0

        return expected_upside / abs(expected_shortfall)

    @cached_property
    def sterling_ratio(self) -> float:
        if self.total_trades < TOTAL_TRADES_THRESHOLD:
            return 0.0

        if len(self.loss) < 2:
            return 0.0

        downside_risk = np.sqrt(np.mean(self.loss**2))

        return (
            self.average_profit / downside_risk
            if downside_risk > SMALL_NUMBER_THRESHOLD
            else 0.0
        )

    @cached_property
    def tail_ratio(self, cutoff=95) -> float:
        if self.total_trades < TOTAL_TRADES_THRESHOLD:
            return 0.0

        denom = np.percentile(self._pnl, 100 - cutoff)

        return (
            abs(np.percentile(self._pnl, cutoff) / denom)
            if abs(denom) > SMALL_NUMBER_THRESHOLD
            else 0.0
        )

    def next(self, pnl: float, fee: float) -> "Performance":
        _pnl, _fee = np.append(self._pnl, pnl), np.append(self._fee, fee)

        return replace(
            self, _pnl=_pnl, _fee=_fee, updated_at=datetime.now().timestamp()
        )

    @staticmethod
    def _max_streak(pnl, winning: bool) -> int:
        pnl_positive = pnl > 0

        mask = pnl_positive == winning

        diff = np.diff(np.concatenate(([0], mask.astype(int), [0])))
        streak_starts = np.where(diff == 1)[0]
        streak_ends = np.where(diff == -1)[0]

        streak_lengths = streak_ends - streak_starts

        return streak_lengths.max() if streak_lengths.size > 0 else 0

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

    def _lpm(self, order: int) -> float:
        downside = np.maximum(0, self._mar - self._pnl)

        return np.mean(downside**order)

    def _hpm(self, order: int) -> float:
        upside = np.maximum(0, self._pnl - self._mar)

        return np.mean(upside**order)
