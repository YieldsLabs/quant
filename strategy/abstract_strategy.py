from abc import ABC, abstractmethod

class AbstractStrategy(ABC):
    def __init__(self):
        pass

    @abstractmethod
    def add_indicators(self, ohlcv):
        pass

    @abstractmethod
    def entry(self, ohlcv):
        pass

    # @abstractmethod
    # def exit(self, ohlcv):
    #     pass