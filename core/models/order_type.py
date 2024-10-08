from enum import Enum, auto


class OrderStatus(Enum):
    PENDING = "pending"
    EXECUTED = "executed"
    FAILED = "failed"
    CLOSED = "closed"

    @classmethod
    def from_raw(cls, value: str) -> "OrderStatus":
        _status_map = {
            "Filled": cls.EXECUTED,
            "New": cls.PENDING,
            "Rejected": cls.FAILED,
            "Cancelled": cls.CLOSED,
        }

        try:
            return _status_map[value]
        except KeyError:
            raise ValueError(f"Unknown order status: '{value}'")


class OrderType(Enum):
    MARKET = auto()
    LIMIT = auto()
    PAPER = auto()

    @classmethod
    def from_raw(cls, value: str) -> "OrderStatus":
        _status_map = {
            "Market": cls.MARKET,
            "Limit": cls.LIMIT,
        }

        try:
            return _status_map[value]
        except KeyError:
            raise ValueError(f"Unknown order status: '{value}'")
