from abc import ABC, abstractmethod
from typing import Optional


class AbstractPositionSizeStrategy(ABC):
    @abstractmethod
    def calculate(self, account_size: float, entry_price: float, trading_fee: float, stop_loss_price: Optional[float] = None,) -> float:
        pass