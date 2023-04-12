from abc import abstractmethod

from shared.meta_label.abstract_meta_label import AbstractMetaLabel
from shared.meta_label.meta_label import meta_label


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
    def call(self, data):
        raise NotImplementedError
