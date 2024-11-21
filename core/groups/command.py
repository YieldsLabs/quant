from enum import Enum, auto


class CommandGroup(Enum):
    account = auto()
    broker = auto()
    portfolio = auto()
    market = auto()
    position = auto()
    factor = auto()

    def __str__(self):
        return self.name
