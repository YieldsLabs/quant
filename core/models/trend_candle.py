from enum import Enum


class TrendCandleType(Enum):
    THREE_CANDLES = 1

    def __str__(self):
        return self.name.upper()