from abc import ABC, abstractmethod
from shared.ohlcv_context import inject_ohlcv


@inject_ohlcv
class AbstractScreening(ABC):
    @abstractmethod
    def run(self):
        raise NotImplementedError