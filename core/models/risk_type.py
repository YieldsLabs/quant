from enum import Enum


class RiskType(Enum):
    TIME = 1
    SIGNAL = 2
    SL = 3
    TP = 4

    def __str__(self):
        return self.name.upper()
