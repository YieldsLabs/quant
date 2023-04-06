from abc import ABC, abstractmethod

import pandas as pd


class AbstractIndicator(ABC):
    @abstractmethod
    def call(self, data: pd.DataFrame):
        raise NotImplementedError
