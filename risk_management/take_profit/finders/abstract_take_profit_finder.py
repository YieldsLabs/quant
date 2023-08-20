from abc import abstractmethod

class AbstractTakeProfit:
    @abstractmethod
    def next(self, entry: float, stop_loss: float):
        pass
