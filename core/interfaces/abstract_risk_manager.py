from abc import abstractmethod

from .abstract_event_manager import AbstractEventManager

from ..models.risk import RiskType
from ..models.ohlcv import OHLCV
from ..models.timeframe import Timeframe
from ..models.position import PositionSide


class AbstractRiskManager(AbstractEventManager):
    @abstractmethod
    def next(self, symbol: str, timeframe: Timeframe, strategy: str, ohlcv: OHLCV, risk_type: RiskType, position_side: PositionSide, position_size: int, entry_price: float, stop_loss_price: float, risk_reward_ratio: float, risk_per_trade: float):
        pass
