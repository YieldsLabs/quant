from abc import ABC, abstractmethod

from ohlcv.context import ohlcv


@ohlcv
class AbstractScreening(ABC):
    @abstractmethod
    def run(self):
        raise NotImplementedError
