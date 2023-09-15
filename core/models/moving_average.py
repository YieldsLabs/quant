from enum import Enum


class MovingAverageType(Enum):
    ALMA = 1
    DEMA = 2
    EMA = 3
    FRAMA = 4
    GMA = 5
    HMA = 6
    RMSMA = 7
    SINWMA = 8
    SMA = 9
    SMMA = 10
    T3 = 11
    TEMA = 12
    TMA = 13
    VWMA = 14
    WMA = 15
    ZLEMA = 16

    def __str__(self):
        return self.name.upper()
