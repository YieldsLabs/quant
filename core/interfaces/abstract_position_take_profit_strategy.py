from abc import ABC, abstractmethod


class AbstractPositionTakeProfitStrategy(ABC):
    @abstractmethod
    def next(self, entry_price: float, stop_loss_price: float) -> float:
        pass