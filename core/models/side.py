from enum import Enum, auto


class PositionSide(Enum):
    LONG = auto()
    SHORT = auto()

    def __str__(self):
        return self.name.upper()


class SignalSide(Enum):
    BUY = auto()
    SELL = auto()

    def __str__(self):
        return self.name.upper()
