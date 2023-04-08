from abc import ABC, abstractmethod


class AbstractAlert(ABC):
    SUFFIX = '_ALERT'
    NAME = ''

    @abstractmethod
    def alert(self, data):
        raise NotImplementedError

    def __str__(self) -> str:
        return f'{self.SUFFIX}{self.NAME}'
