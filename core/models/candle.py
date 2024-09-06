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


class CandleReversalType(Enum):
    DOJI = 1
    ENGULFING = 2
    EUPHORIA = 3
    HAMMER = 4
    HARAMIF = 5
    HARAMIS = 6
    KANGAROO = 7
    R = 8
    SPLIT = 9
    TWEEZERS = 10

    def __str__(self):
        return self.name.upper()
