from enum import Enum


class TrendCandleType(Enum):
    BOTTLE = 1
    DOUBLE_TROUBLE = 2
    GOLDEN = 3
    H = 4
    HIKKAKE = 5
    MARUBOZU = 6
    MASTER_CANDLE = 7
    SLINGSHOT = 8
    THREE_CANDLES = 9
    THREE_METHODS = 10
    TASUKI = 11

    def __str__(self):
        return self.name.upper()