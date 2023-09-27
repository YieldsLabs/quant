from enum import Enum


class MarginMode(Enum):
    ISOLATED = "isolated"
    CROSS = "cross"


class PositionMode(Enum):
    ONE_WAY = "one way"
    HEDGED = "hedged"
