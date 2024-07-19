from enum import Enum


class CandleTrendType(Enum):
    BOTTLE = 1
    DOUBLE_TROUBLE = 2
    GOLDEN = 3
    H = 4
    HEXAD = 5
    HIKKAKE = 6
    MARUBOZU = 7
    MASTER_CANDLE = 8
    QUINTUPLETS = 9
    SLINGSHOT = 10
    THREE_CANDLES = 11
    THREE_METHODS = 12
    TASUKI = 13
    THREE_ONE_TWO = 14

    def __str__(self):
        return self.name.upper()


class CandleContrarianType(Enum):
    R = 1

    def __str__(self):
        return self.name.upper()
