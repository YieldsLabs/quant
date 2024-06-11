from enum import Enum


class MovingAverageType(Enum):
    ALMA = 1
    CAMA = 2
    DEMA = 3
    EMA = 4
    FRAMA = 5
    GMA = 6
    HMA = 7
    HEMA = 8
    KAMA = 9
    KJS = 10
    LSMA = 11
    MD = 12
    RMSMA = 13
    SINWMA = 14
    SMA = 15
    SMMA = 16
    T3 = 17
    TEMA = 18
    TRIMA = 19
    VIDYA = 20
    VWMA = 21
    VWEMA = 22
    WMA = 23
    ZLEMA = 24
    ZLSMA = 25
    ZLTEMA = 26
    ZLHMA = 27

    def __str__(self):
        return self.name.upper()
