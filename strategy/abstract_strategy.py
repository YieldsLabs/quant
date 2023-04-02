from abc import ABC, abstractmethod

from shared.ohlcv_context import inject_ohlcv

@inject_ohlcv
class AbstractStrategy(ABC):
    @abstractmethod
    def entry(self):
        raise NotImplementedError