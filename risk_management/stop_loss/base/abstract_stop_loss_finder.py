from abc import ABC, abstractmethod
from ohlcv.context import ohlcv
from shared.position_side import PositionSide


@ohlcv
class AbstractStopLoss(ABC):
    SUFFIX = "_STOPLOSS"
    NAME = ""

    @abstractmethod
    def next(self, position_side: PositionSide, entry_price: float):
        pass

    def __str__(self) -> str:
        return f'{self.SUFFIX}{self.NAME}'
