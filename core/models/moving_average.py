from enum import Enum


class MovingAverageType(Enum):
    ALMA = 1
    CAMA = 2
    DEMA = 3
    EMA = 4
    FRAMA = 5
    GMA = 6
    HMA = 7
    KAMA = 8
    KJS = 9
    LSMA = 10
    MD = 11
    RMSMA = 12
    SINWMA = 13
    SMA = 14
    SMMA = 15
    T3 = 16
    TEMA = 17
    TMA = 18
    VIDYA = 19
    VWMA = 20
    VWEMA = 21
    WMA = 22
    ZLEMA = 23
    ZLSMA = 24
    ZLTEMA = 25
    ZLHMA = 26

    def __str__(self):
        return self.name.upper()
