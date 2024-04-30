from enum import Enum


class SourceType(Enum):
    CLOSE = 1
    HL2 = 2
    HLC3 = 3
    HLCC4 = 4
    OHLC4 = 5

    def __str__(self):
        return self.name.upper()
