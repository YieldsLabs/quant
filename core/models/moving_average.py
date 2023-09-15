from enum import Enum


class MovingAverageType(Enum):
    ALMA = 1
    DEMA = 2
    EMA = 3
    FRAMA = 4
    GMA = 5
    HMA = 6
    KAMA = 7
    RMSMA = 8
    SINWMA = 9
    SMA = 10
    SMMA = 11
    T3 = 12
    TEMA = 13
    TMA = 14
    VWMA = 15
    WMA = 16
    ZLEMA = 17

    def __str__(self):
        return self.name.upper()
