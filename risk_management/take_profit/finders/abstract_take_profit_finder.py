from abc import abstractmethod

from labels.abstract_meta_label import AbstractMetaLabel
from labels.meta_label import meta_label


@meta_label
class AbstractTakeProfit(AbstractMetaLabel):
    SUFFIX = "_TKPRFT"
    NAME = ""

    @abstractmethod
    def next(self, entry: float, stop_loss: float):
        pass
