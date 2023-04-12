from abc import ABC, abstractmethod

import pandas as pd

from shared.meta_label.abstract_meta_label import AbstractMetaLabel
from shared.meta_label.meta_label import meta_label


@meta_label
class AbstractIndicator(AbstractMetaLabel):
    SUFFIX = "_IND"
    NAME = ""

    @abstractmethod
    def call(self, data: pd.DataFrame):
        raise NotImplementedError
