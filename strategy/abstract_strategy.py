from abc import abstractmethod

import pandas as pd
from shared.meta_label.abstract_meta_label import AbstractMetaLabel
from shared.meta_label.meta_label import meta_label


@meta_label
class AbstractStrategy(AbstractMetaLabel):
    SUFFIX = '_STRATEGY'
    NAME = ""

    @abstractmethod
    def entry(self, ohlcv: pd.DataFrame):
        raise NotImplementedError

    @abstractmethod
    def exit(self, ohlcv: pd.DataFrame):
        raise NotImplementedError
