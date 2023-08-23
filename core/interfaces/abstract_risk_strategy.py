from abc import ABC, abstractmethod

from ..models.ohlcv import OHLCV
from ..models.position import PositionSide


class AbstractRiskStrategy(ABC):
    @abstractmethod
    def next(self, strategy: str, position_side: PositionSide, position_size: float, stop_loss_price: float, entry_price: float, risk_per_trade: float, ohlcv: OHLCV) -> float:
        pass
    
    @abstractmethod
    def reset(self, strategy: str, position_side: PositionSide):
        pass