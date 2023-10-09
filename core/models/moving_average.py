from enum import Enum


class MovingAverageType(Enum):
    ALMA = 1
    DEMA = 2
    EMA = 3
    FRAMA = 4
    GMA = 5
    HMA = 6
    KAMA = 7
    LSMA = 8
    RMSMA = 9
    SINWMA = 10
    SMA = 11
    SMMA = 12
    T3 = 13
    TEMA = 14
    TMA = 15
    VWMA = 16
    WMA = 17
    ZLEMA = 18

    def __str__(self):
        return self.name.upper()
