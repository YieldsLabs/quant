from enum import Enum


class RSIType(Enum):
    RSI = 1

    def __str__(self):
        return self.name.upper()
