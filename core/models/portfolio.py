import numpy as np
from dataclasses import asdict, dataclass, field, replace


@dataclass(frozen=True)
class Performance:
    _account_size: float
    _risk_per_trade: float
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
    def hit_ratio(self):
        pnl_positive = self._pnl > 0
        successful_trades = pnl_positive.sum()

        return 100 * (successful_trades / self.total_trades)
    
    @property
    def risk_of_ruin(self):
        win_rate = self.hit_ratio / 100

        if win_rate == 1 or win_rate == 0:
            return 0

        loss_rate = 1 - win_rate

        return ((1 - (self._risk_per_trade * (1 - loss_rate / win_rate))) ** self._account_size) * 100
    
    @property
    def max_consecutive_wins(self):
        return self._max_streak(self._pnl, True)
    
    @property
    def max_consecutive_losses(self):
        return self._max_streak(self._pnl, False)
    
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
    
    def __repr__(self):
        return (f"Performance(total_trades={self.total_trades}, hit_ratio={self.hit_ratio}, risk_of_ruin={self.risk_of_ruin}, total_pnl={self.total_pnl}, average_pnl={self.average_pnl}, max_consecutive_wins={self.max_consecutive_wins}, max_consecutive_losses={self.max_consecutive_losses})")

