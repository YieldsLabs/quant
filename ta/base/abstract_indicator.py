from abc import ABC, abstractmethod

import pandas as pd


class AbstractIndicator(ABC):
    SUFFIX = "_INDICATOR"
    NAME = ""

    @abstractmethod
    def call(self, data: pd.DataFrame):
        raise NotImplementedError

    def __str__(self) -> str:
        return f'{self.SUFFIX}{self.NAME}'
