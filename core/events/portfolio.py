from dataclasses import asdict, dataclass
from datetime import datetime, time
from .ohlcv import OHLCV
from .position import PositionSide
from ..timeframe import Timeframe
from ..event_dispatcher import Event

@dataclass(frozen=True)
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

    def to_dict(self):
        return asdict(self)


@dataclass(frozen=True, eq=True)
class PortfolioPerformanceEvent(Event):
    id: str
    performance: PortfolioPerformance
    timestamp: int = datetime.now().timestamp()


@dataclass(frozen=True, eq=True)
class BestStrategyEvent(PortfolioPerformanceEvent):
    pass

@dataclass(frozen=True, eq=True)
class CheckExitConditions(Event):
    symbol: str
    timeframe: Timeframe
    side: PositionSide
    size: float
    entry: float
    stop_loss: float
    take_profit: float
    risk: float
    ohlcv: OHLCV
    timestamp: int = datetime.now().timestamp()
