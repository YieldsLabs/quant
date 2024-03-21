from enum import Enum


class MovingAverageType(Enum):
    ALMA = 1
    DEMA = 2
    EMA = 3
    FRAMA = 4
    GMA = 5
    HMA = 6
    KAMA = 7
    KJS = 8
    LSMA = 9
    MD = 10
    RMSMA = 11
    SINWMA = 12
    SMA = 13
    SMMA = 14
    T3 = 15
    TEMA = 16
    TMA = 17
    VIDYA = 18
    VWMA = 19
    WMA = 20
    ZLEMA = 21
    ZLSMA = 22
    ZLTEMA = 23
    ZLHMA = 24

    def __str__(self):
        return self.name.upper()
