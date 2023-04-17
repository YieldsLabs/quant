from abc import ABC


class AbstractMetaLabel(ABC):
    SUFFIX = "_"
    NAME = ""

    def __str__(self) -> str:
        return f'{self.SUFFIX}{self.NAME}'
