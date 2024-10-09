from enum import Enum, auto


class DataSourceType(Enum):
    BYBIT = auto()

    def __str__(self):
        return self.name.upper()
