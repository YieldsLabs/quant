from abc import ABC, abstractmethod
from ohlcv.context import ohlcv
from shared.position_side import PositionSide


@ohlcv
class AbstractStopLoss(ABC):
    @abstractmethod
    def next(self, position_side: PositionSide, entry_price: float):
        pass