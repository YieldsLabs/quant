from abc import ABC, abstractmethod


class AbstractStopLoss(ABC):
    @abstractmethod
    def set_ohlcv(self, data):
        pass

    @abstractmethod
    def next(self, entry_trade_type, entry_price):
        pass

    @abstractmethod
    def reset(self):
        pass