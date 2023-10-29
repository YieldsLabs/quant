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
    MD = 9
    RMSMA = 10
    SINWMA = 11
    SMA = 12
    SMMA = 13
    T3 = 14
    TEMA = 15
    TMA = 16
    VWMA = 17
    WMA = 18
    ZLEMA = 19
    ZLSMA = 20

    def __str__(self):
        return self.name.upper()
