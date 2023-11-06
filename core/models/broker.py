from enum import Enum, auto


class MarginMode(Enum):
    ISOLATED = "isolated"
    CROSS = "cross"


class PositionMode(Enum):
    ONE_WAY = "one way"
    HEDGED = "hedged"


class BrokerType(Enum):
    FUTURES = auto()
