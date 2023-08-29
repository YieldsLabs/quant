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

    def next(self, pnl: float) -> 'Performance':
        _pnl = np.append(self._pnl, pnl)
        
        return replace(
            self,
            _pnl = _pnl
        )
    
    def __repr__(self):
        return (f"Performance(total_trades={self.total_trades}, hit_ratio={self.hit_ratio}, total_pnl={self.total_pnl}, average_pnl={self.average_pnl})")

