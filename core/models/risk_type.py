import re
from enum import Enum, auto


class PositionRiskType(Enum):
    NONE = 0
    TIME = 1
    SIGNAL = 2
    SL = 3
    TP = 4

    def __str__(self):
        return self.name.upper()


class SignalRiskType(Enum):
    NONE = auto()
    LOW = auto()
    MODERATE = auto()
    HIGH = auto()

    @classmethod
    def from_string(cls, risk_string):
        match = re.search(r"\b(NONE|LOW|MODERATE|HIGH)\b(?![a-zA-Z0-9])", risk_string)

        if match:
            return cls[match.group()]
        else:
            return cls.NONE

    def __str__(self):
        return self.name.upper()


class SessionRiskType(Enum):
    CONTINUE = auto()
    EXIT = auto()

    def __str__(self):
        return self.name.upper()
