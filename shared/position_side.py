from enum import Enum

class PositionSide(Enum):
    LONG = "long"
    SHORT = "short"

    def __str__(self):
        return self.value