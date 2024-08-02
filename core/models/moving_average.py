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
    SLSMA = 15
    SMA = 16
    SMMA = 17
    T3 = 18
    TEMA = 19
    TL = 20
    TRIMA = 21
    ULTS = 22
    VIDYA = 23
    VWMA = 24
    VWEMA = 25
    WMA = 26
    ZLEMA = 27
    ZLSMA = 28
    ZLTEMA = 29
    ZLHMA = 30

    def __str__(self):
        return self.name.upper()
