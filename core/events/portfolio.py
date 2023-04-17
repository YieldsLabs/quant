from dataclasses import asdict, dataclass
from core.events.ohlcv import OHLCV

from core.events.position import PositionSide
from core.timeframes import Timeframes

from ..event_dispatcher import Event

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

    def to_dict(self):
        return asdict(self)


@dataclass
class PortfolioPerformanceEvent(Event):
    id: str
    performance: PortfolioPerformance

@dataclass
class CheckExitConditions(Event):
    symbol: str
    timeframe: Timeframes
    side: PositionSide
    size: float
    entry: float
    stop_loss: float
    take_profit: float
    risk: float
    ohlcv: OHLCV