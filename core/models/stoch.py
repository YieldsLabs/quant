from enum import Enum


class StochType(Enum):
    STOCHOSC = 1

    def __str__(self):
        return self.name.upper()
