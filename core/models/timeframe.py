from enum import Enum


class Timeframe(Enum):
    ONE_MINUTE = "1m"
    THREE_MINUTES = "3m"
    FIVE_MINUTES = "5m"
    FIFTEEN_MINUTES = "15m"
    ONE_HOUR = "1h"
    FOUR_HOURS = "4h"

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
