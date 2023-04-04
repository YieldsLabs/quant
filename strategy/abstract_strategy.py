from abc import ABC, abstractmethod

import pandas as pd


class AbstractStrategy(ABC):
    @abstractmethod
    def entry(self, ohlcv: pd.DataFrame):
        raise NotImplementedError

    @abstractmethod
    def exit(self, ohlcv: pd.DataFrame):
        raise NotImplementedError
