from enum import Enum


class MACDType(Enum):
    MACD = 1

    def __str__(self):
        return self.name.upper()
