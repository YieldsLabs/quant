from enum import Enum


class MovingAverageType(Enum):
    SMA = 1
    EMA = 2
    WMA = 3
    ZLEMA = 4
    HMA = 5
    VWMA = 6
    DEMA = 7
    TEMA = 8

    def __str__(self):
        return self.name.upper()
