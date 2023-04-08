from abc import ABC

from shared.meta_label import determine_type


class AbstractMetaLabel(ABC):
    SUFFIX = "_"
    NAME = ""

    def __init__(self):
        pass

    def __str__(self) -> str:
        return f'{self.SUFFIX}{self.NAME}'

    @classmethod
    def from_label(cls, encoded_label: str):
        parts = encoded_label.split(f"{cls.__str__()}")[1].split("_")[0]
        name = ''.join([c for c in parts if c.isalpha()])
        params = parts[len(name):].split(":")
        args = [determine_type(param) for param in params]

        return cls(*args)
