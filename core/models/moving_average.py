from enum import Enum


class MovingAverageType(Enum):
    ALMA = 1
    DEMA = 2
    EMA = 3
    FRAMA = 4
    GMA = 5
    HMA = 6
    RMSMA = 7
    SMA = 8
    SMMA = 9
    T3 = 10
    TEMA = 11
    TMA = 12
    VWMA = 13
    WMA = 14
    ZLEMA = 15

    def __str__(self):
        return self.name.upper()
