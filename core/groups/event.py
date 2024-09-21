from enum import Enum, auto


class EventGroup(Enum):
    account = auto()
    backtest = auto()
    market = auto()
    portfolio = auto()
    position = auto()
    risk = auto()
    service = auto()
    signal = auto()
    system = auto()

    def __str__(self):
        return self.name
