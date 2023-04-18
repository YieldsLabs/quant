from enum import Enum


class Timeframe(Enum):
    ONE_MINUTE = '1m'
    THREE_MINUTES = '3m'
    FIVE_MINUTES = '5m'
    FIFTEEN_MINUTES = '15m'
    ONE_HOUR = '1H'
    FOUR_HOURS = '4H'

    def __str__(self):
        return self.value
