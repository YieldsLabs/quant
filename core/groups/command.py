from enum import Enum, auto


class CommandGroup(Enum):
    account = auto()
    broker = auto()
    portfolio = auto()
    feed = auto()
    market = auto()

    def __str__(self):
        return self.name
