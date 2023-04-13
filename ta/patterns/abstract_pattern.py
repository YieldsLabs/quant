from abc import ABC, abstractmethod

from shared.meta_label.abstract_meta_label import AbstractMetaLabel
from shared.meta_label.meta_label import meta_label


@meta_label
class AbstractPattern(AbstractMetaLabel):
    SUFFIX = "_PTTRN"
    NAME = ""

    @classmethod
    def bullish_column(cls) -> str:
        return f'{cls.NAME}_BULLISH'

    @classmethod
    def bearish_column(cls) -> str:
        return f'{cls.NAME}_BEARISH'

    @abstractmethod
    def bullish(self, data) -> bool:
        raise NotImplementedError

    @abstractmethod
    def bearish(self, data) -> bool:
        raise NotImplementedError
