from enum import Enum, auto


class OrderStatus(Enum):
    PENDING = "pending"
    EXECUTED = "executed"
    FAILED = "failed"
    CLOSED = "closed"


class OrderType(Enum):
    MARKET = auto()
    PAPER = auto()
