from enum import Enum

class TradeType(Enum):
    LONG = 'long'
    SHORT = 'short'
    BOTH = 'both'

    def __str__(self):
        return self.value