from abc import ABC, abstractmethod
from shared.ohlcv_context import inject_ohlcv

from shared.trade_type import TradeType

@inject_ohlcv
class AbstractStopLoss(ABC):
    @abstractmethod
    def next(self, entry_trade_type: TradeType, entry_price: float):
        pass
    
    @abstractmethod
    def reset(self):
        pass