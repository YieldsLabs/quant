from enum import Enum


class MovingAverageType(Enum):
    # ALMA = 1
    CAMA = 2
    # DEMA = 3
    # EMA = 4
    FRAMA = 5
    # GMA = 6
    # HMA = 7
    # HEMA = 8
    # KAMA = 9
    # KJS = 10
    # LSMA = 11
    # MD = 12
    # RMSMA = 13
    # SINWMA = 14
    # SMA = 15
    # SMMA = 16
    T3 = 17
    TEMA = 18
    # TL = 19
    TRIMA = 20
    ULTS = 21
    VIDYA = 22
    # VWMA = 23
    # VWEMA = 24
    # WMA = 25
    # ZLEMA = 26
    ZLSMA = 27
    ZLTEMA = 28
    # ZLHMA = 29

    def __str__(self):
        return self.name.upper()
