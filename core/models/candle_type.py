from enum import Enum, auto


class CandleType(Enum):
    BULLISH = auto()
    BEARISH = auto()
    NEUTRAL = auto()

    def __str__(self):
        return self.name.upper()
