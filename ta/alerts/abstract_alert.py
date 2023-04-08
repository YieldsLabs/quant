from abc import abstractmethod

from shared.meta_label.abstract_meta_label import AbstractMetaLabel
from shared.meta_label.meta_label import meta_label


@meta_label
class AbstractAlert(AbstractMetaLabel):
    SUFFIX = '_ALERT'
    NAME = ''

    @abstractmethod
    def alert(self, data):
        raise NotImplementedError
