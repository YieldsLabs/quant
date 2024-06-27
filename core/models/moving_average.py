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
    VIDYA = 21
    # VWMA = 22
    # VWEMA = 23
    # WMA = 24
    # ZLEMA = 25
    ZLSMA = 26
    ZLTEMA = 27
    # ZLHMA = 28

    def __str__(self):
        return self.name.upper()
