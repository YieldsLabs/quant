from abc import abstractmethod
from typing import Tuple

import pandas as pd
from core.events.ohlcv import OHLCV
from labels.abstract_meta_label import AbstractMetaLabel

from labels.meta_label import meta_label


@meta_label
class AbstractStopLoss(AbstractMetaLabel):
    SUFFIX = "_STPLSS"
    NAME = ""

    @abstractmethod
    def next(self, entry: float, ohlcv: pd.DataFrame) -> Tuple[float, float]:
        pass
