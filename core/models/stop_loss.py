from enum import Enum


class StopLossType(Enum):
    ATR = 1

    def __str__(self):
        return self.name.upper()
