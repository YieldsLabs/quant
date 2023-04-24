from abc import abstractmethod
from typing import Tuple
from labels.abstract_meta_label import AbstractMetaLabel

from labels.meta_label import meta_label


@meta_label
class AbstractAlert(AbstractMetaLabel):
    SUFFIX = '_ALRT'
    NAME = ''

    @classmethod
    def buy_column(cls) -> str:
        return f'{cls.NAME}_BUY'

    @classmethod
    def sell_column(cls) -> str:
        return f'{cls.NAME}_SELL'

    @abstractmethod
    def call(self, data) -> Tuple[bool, bool]:
        raise NotImplementedError
