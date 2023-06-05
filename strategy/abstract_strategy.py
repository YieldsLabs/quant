from abc import abstractmethod
from typing import Tuple
import pandas as pd

from labels.abstract_meta_label import AbstractMetaLabel
from labels.meta_label import meta_label


@meta_label
class AbstractStrategy(AbstractMetaLabel):
    SUFFIX = '_STRTG'
    NAME = ""

    @abstractmethod
    def entry(self, ohlcv: pd.DataFrame) -> Tuple[bool, bool]:
        pass

    @abstractmethod
    def exit(self, ohlcv: pd.DataFrame) -> Tuple[bool, bool]:
        pass

    @abstractmethod
    def stop_loss(self, entry: float, ohlcv: pd.DataFrame) -> Tuple[float, float]:
        pass
