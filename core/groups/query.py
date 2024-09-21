from enum import Enum, auto


class QueryGroup(Enum):
    account = auto()
    broker = auto()
    position = auto()
    portfolio = auto()
    copilot = auto()
    market = auto()
    ta = auto()

    def __str__(self):
        return self.name
