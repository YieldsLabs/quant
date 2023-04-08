from abc import ABC, abstractmethod


class AbstractPattern(ABC):
    SUFFIX = "_PATTERN"
    NAME = ""

    @abstractmethod
    def bullish(self, data):
        raise NotImplementedError

    @abstractmethod
    def bearish(self, data):
        raise NotImplementedError

    def __str__(self) -> str:
        return f'{self.SUFFIX}{self.NAME}'
