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
    INSANE = auto()

    @classmethod
    def from_string(cls, risk_string):
        risk_mapping = {
            "NONE": cls.NONE,
            "LOW": cls.LOW,
            "MODERATE": cls.MODERATE,
            "HIGH": cls.HIGH,
            "INSANE": cls.INSANE,
        }

        return risk_mapping.get(risk_string.upper(), None)

    def __str__(self):
        return self.name.upper()


class SessionRiskType(Enum):
    CONTINUE = auto()
    EXIT = auto()

    def __str__(self):
        return self.name.upper()
