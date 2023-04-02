from abc import ABC, abstractmethod

from shared.trade_type import TradeType


class AbstractStopLoss(ABC):
    @abstractmethod
    def set_ohlcv(self, data):
        pass

    @abstractmethod
    def next(self, entry_trade_type: TradeType, entry_price: float):
        pass

    @abstractmethod
    def reset(self):
        pass