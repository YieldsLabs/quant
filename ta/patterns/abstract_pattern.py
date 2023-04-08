from abc import ABC, abstractmethod

from shared.meta_label.abstract_meta_label import AbstractMetaLabel
from shared.meta_label.meta_label import meta_label


@meta_label
class AbstractPattern(AbstractMetaLabel):
    SUFFIX = "_PATTERN"
    NAME = ""

    @abstractmethod
    def bullish(self, data):
        raise NotImplementedError

    @abstractmethod
    def bearish(self, data):
        raise NotImplementedError
