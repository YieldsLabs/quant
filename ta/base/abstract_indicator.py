from abc import abstractmethod

import pandas as pd
from labels.abstract_meta_label import AbstractMetaLabel

from labels.meta_label import meta_label


@meta_label
class AbstractIndicator(AbstractMetaLabel):
    SUFFIX = "_IND"
    NAME = ""

    @abstractmethod
    def call(self, data: pd.DataFrame):
        raise NotImplementedError
