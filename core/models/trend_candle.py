from enum import Enum


class TrendCandleType(Enum):
    BOTTLE = 1
    DOUBLE_TROUBLE = 2
    GOLDEN = 3
    H = 4
    HIKKAKE = 5
    MARUBOZU = 6
    MASTER_CANDLE = 7
    QUINTUPLETS = 8
    SLINGSHOT = 9
    THREE_CANDLES = 10
    THREE_METHODS = 11
    TASUKI = 12

    def __str__(self):
        return self.name.upper()