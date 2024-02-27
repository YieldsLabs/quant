from enum import Enum


class Timeframe(Enum):
    ONE_MINUTE = "1m"
    THREE_MINUTES = "3m"
    FIVE_MINUTES = "5m"
    FIFTEEN_MINUTES = "15m"
    ONE_HOUR = "1h"
    FOUR_HOURS = "4h"

    @classmethod
    def from_raw(cls, value: str) -> "Timeframe":
        for timeframe in cls:
            if timeframe.value == value:
                return timeframe

        raise ValueError(f"No matching Timeframe for value: {value}")

    def __str__(self):
        return self.value

    def __repr__(self) -> str:
        return f"Timeframe({self.value})"

    def __lt__(self, other):
        if not isinstance(other, Timeframe):
            return NotImplemented

        return self._member_names_.index(self.name) < self._member_names_.index(
            other.name
        )

    def __hash__(self) -> int:
        return hash(self.value)
