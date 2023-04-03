from abc import ABC, abstractmethod
from shared.ohlcv_context import inject_ohlcv
from shared.position_side import PositionSide


@inject_ohlcv
class AbstractStopLoss(ABC):
    @abstractmethod
    def next(self, position_side: PositionSide, entry_price: float):
        pass
    
    @abstractmethod
    def reset(self):
        pass