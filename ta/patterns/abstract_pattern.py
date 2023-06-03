from abc import abstractmethod

from labels.abstract_meta_label import AbstractMetaLabel
from labels.meta_label import meta_label


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
        pass

    @abstractmethod
    def bearish(self, data) -> bool:
        pass
