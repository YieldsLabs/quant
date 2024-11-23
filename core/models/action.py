from enum import Enum


class Action(Enum):
    GO_LONG = 1
    GO_SHORT = 2
    DO_NOTHING = 0

    @classmethod
    def from_raw(cls, value: float):
        for action in cls:
            if action.value == value:
                return action

        raise ValueError(f"No matching Action for float value: {value}")

    def __str__(self):
        return self.name
