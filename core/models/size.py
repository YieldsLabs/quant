from enum import Enum, auto


class PositionSizeType(Enum):
    Fixed = auto()
    Kelly = auto()

    def __str__(self):
        return self.name.upper()
