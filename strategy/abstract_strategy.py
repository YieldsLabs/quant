from abc import ABC, abstractmethod

class AbstractStrategy(ABC):
    @abstractmethod
    def entry(self, ohlcv):
        pass