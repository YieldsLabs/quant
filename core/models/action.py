from enum import Enum


class Action(Enum):
    GO_LONG = 1.0
    GO_SHORT = 2.0
    EXIT_LONG = 3.0
    EXIT_SHORT = 4.0
    DO_NOTHING = 0.0

    @classmethod
    def from_raw(cls, value: float):
        for action in cls:
            if action.value == value:
                return action

        raise ValueError(f"No matching Action for float value: {value}")

    def __str__(self):
        return self.name
