

from enum import Enum, auto


class StrategyType(Enum):
    TREND_FOLLOW = "Trend Follow"
    CONTRARIAN = "Contrarian"

    def __str__(self):
        return self.value