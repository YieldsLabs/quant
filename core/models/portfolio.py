import numpy as np
from dataclasses import asdict, dataclass, field, replace


@dataclass(frozen=True)
class Performance:
    _account_size: float
    _risk_per_trade: float
    _periods_per_year: float = 252
    _pnl: np.array = field(default_factory=lambda: np.array([]))

    @property
    def total_trades(self):
        return self._pnl.size

    @property
    def total_pnl(self):
        return self._pnl.sum()
    
    @property
    def average_pnl(self):
        return self._pnl.mean()
    
    @property
    def max_consecutive_wins(self):
        return self._max_streak(self._pnl, True)
    
    @property
    def max_consecutive_losses(self):
        return self._max_streak(self._pnl, False)
    
    @property
    def hit_ratio(self):
        pnl_positive = self._pnl > 0
        successful_trades = pnl_positive.sum()

        return 100 * (successful_trades / self.total_trades)
    
    @property
    def max_drawdown(self) -> float:
        account_size = self._account_size

        peak = account_size
        max_drawdown = 0

        for pnl_value in self._pnl:
            account_size += pnl_value
            peak = max(peak, account_size)
            drawdown = (peak - account_size) / peak
            max_drawdown = max(max_drawdown, drawdown)

        return max_drawdown
    
    @property
    def calmar_ratio(self) -> float:
        if self.max_drawdown == 0:
            return 0

        rate_of_return = self._rate_of_return(self._account_size, self.total_pnl)
        
        return rate_of_return / abs(self.max_drawdown)
    
    @property
    def annualized_return(self) -> float:
        rate_of_return = self._rate_of_return(self._account_size, self.total_pnl)

        if rate_of_return < 0 and self._periods_per_year % self.total_trades != 0:
            return 0

        holding_period_return = 1 + rate_of_return
        annualized_return = holding_period_return ** (self._periods_per_year / self.total_trades) - 1

        return annualized_return
    
    @property
    def annualized_volatility(self) -> float:
        if self.total_trades < 2:
            return 0

        daily_returns = self._pnl / self._account_size
        volatility = np.std(daily_returns, ddof=1)
        annualized_volatility = volatility * np.sqrt(self._periods_per_year)

        return annualized_volatility
    
    @property
    def recovery_factor(self) -> float:
        total_profit = self._pnl[self._pnl > 0].sum()

        return total_profit /self.max_drawdown if self.max_drawdown != 0 else 0
    
    @property
    def risk_of_ruin(self):
        win_rate = self.hit_ratio / 100

        if win_rate == 1 or win_rate == 0:
            return 0

        loss_rate = 1 - win_rate

        return ((1 - (self._risk_per_trade * (1 - loss_rate / win_rate))) ** self._account_size) * 100
    
    def next(self, pnl: float) -> 'Performance':
        _pnl = np.append(self._pnl, pnl)
        
        return replace(
            self,
            _pnl = _pnl
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
    def _rate_of_return(initial_account_size, total_pnl) -> float:
        account_size = initial_account_size + total_pnl

        return (account_size / initial_account_size) - 1
    
    def __repr__(self):
        return (f"Performance(total_trades={self.total_trades}, hit_ratio={self.hit_ratio}, " +
                 f"max_drawdown={self.max_drawdown}, calmar_ratio={self.calmar_ratio}, " +
                 f"risk_of_ruin={self.risk_of_ruin}, recovery_factor={self.recovery_factor}, " +
                 f"total_pnl={self.total_pnl}, average_pnl={self.average_pnl}, " +
                 f"max_consecutive_wins={self.max_consecutive_wins}, max_consecutive_losses={self.max_consecutive_losses}, " +
                 f"annualized_return={self.annualized_return}, annualized_volatility={self.annualized_volatility}, " + 
                 f")")
    
    def to_dict(self):
        return asdict(self)

