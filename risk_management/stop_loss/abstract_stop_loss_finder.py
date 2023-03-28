from abc import ABC, abstractmethod


class AbstractStopLoss(ABC):
    @abstractmethod
    def set_ohlcv():
        pass

    @abstractmethod
    def next():
        pass

    @abstractmethod
    def reset():
        pass