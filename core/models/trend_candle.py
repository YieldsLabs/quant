from enum import Enum


class TrendCandleType(Enum):
    BOTTLE = 1
    DOUBLE_TROUBLE = 2
    GOLDEN = 3
    H = 4
    MARUBOZU = 5
    MASTER_CANDLE = 6
    SLINGSHOT = 7
    THREE_CANDLES = 8
    TASUKI = 9

    def __str__(self):
        return self.name.upper()