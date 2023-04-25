from dataclasses import asdict, dataclass, field

from .base_event import Event, EventMeta


@dataclass
class PortfolioPerformance:
    total_trades: int
    successful_trades: int
    win_rate: float
    risk_of_ruin: float
    rate_of_return: float
    total_pnl: float
    average_pnl: float
    sharpe_ratio: float
    sortino_ratio: float
    profit_factor: float
    max_consecutive_wins: int
    max_consecutive_losses: int
    max_drawdown: float
    recovery_factor: float
    skewness: float
    kurtosis: float
    calmar_ratio: float
    cvar: float
    ulcer_index: float

    def to_dict(self):
        return asdict(self)


@dataclass(frozen=True)
class PortfolioPerformanceEvent(Event):
    strategy_id: str
    performance: PortfolioPerformance
    meta: EventMeta = field(default_factory=lambda: EventMeta(priority=4))
