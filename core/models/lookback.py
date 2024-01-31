from enum import Enum

from .timeframe import Timeframe


class Lookback(Enum):
    ONE_MONTH = "1M"
    TWO_MONTH = "2M"
    THREE_MONTH = "3M"
    FOUR_MONTH = "4M"
    FIVE_MONTH = "5M"
    SIX_MONTH = "6M"
    SEVEN_MONTH = "7M"
    EIGHT_MONTH = "8M"
    NINE_MONTH = "9M"
    TEN_MONTH = "10M"
    ELEVEN_MONTH = "11M"
    ONE_YEAR = "1Y"

    @classmethod
    def from_raw(cls, value: str) -> "Lookback":
        for lookback in cls:
            if lookback.value == value:
                return lookback

        raise ValueError(f"No matching Lookback for value: {value}")

    def __str__(self):
        return self.value


TIMEFRAMES_TO_LOOKBACK = {
    (Lookback.ONE_MONTH, Timeframe.ONE_MINUTE): 43200,
    (Lookback.ONE_MONTH, Timeframe.FIVE_MINUTES): 8640,
    (Lookback.ONE_MONTH, Timeframe.FIFTEEN_MINUTES): 2880,
    (Lookback.ONE_MONTH, Timeframe.ONE_HOUR): 720,
    (Lookback.TWO_MONTH, Timeframe.ONE_MINUTE): 43200 * 2,
    (Lookback.TWO_MONTH, Timeframe.FIVE_MINUTES): 8640 * 2,
    (Lookback.TWO_MONTH, Timeframe.FIFTEEN_MINUTES): 2880 * 2,
    (Lookback.TWO_MONTH, Timeframe.ONE_HOUR): 720 * 2,
    (Lookback.THREE_MONTH, Timeframe.ONE_MINUTE): 43200 * 3,
    (Lookback.THREE_MONTH, Timeframe.FIVE_MINUTES): 8640 * 3,
    (Lookback.THREE_MONTH, Timeframe.FIFTEEN_MINUTES): 2880 * 3,
    (Lookback.THREE_MONTH, Timeframe.ONE_HOUR): 720 * 3,
    (Lookback.FOUR_MONTH, Timeframe.ONE_MINUTE): 43200 * 4,
    (Lookback.FOUR_MONTH, Timeframe.FIVE_MINUTES): 8640 * 4,
    (Lookback.FOUR_MONTH, Timeframe.FIFTEEN_MINUTES): 2880 * 4,
    (Lookback.FOUR_MONTH, Timeframe.ONE_HOUR): 720 * 4,
    (Lookback.FIVE_MONTH, Timeframe.ONE_MINUTE): 43200 * 5,
    (Lookback.FIVE_MONTH, Timeframe.FIVE_MINUTES): 8640 * 5,
    (Lookback.FIVE_MONTH, Timeframe.FIFTEEN_MINUTES): 2880 * 5,
    (Lookback.FIVE_MONTH, Timeframe.ONE_HOUR): 720 * 5,
    (Lookback.SIX_MONTH, Timeframe.ONE_MINUTE): 43200 * 6,
    (Lookback.SIX_MONTH, Timeframe.FIVE_MINUTES): 8640 * 6,
    (Lookback.SIX_MONTH, Timeframe.FIFTEEN_MINUTES): 2880 * 6,
    (Lookback.SIX_MONTH, Timeframe.ONE_HOUR): 720 * 6,
    (Lookback.SEVEN_MONTH, Timeframe.ONE_MINUTE): 43200 * 7,
    (Lookback.SEVEN_MONTH, Timeframe.FIVE_MINUTES): 8640 * 7,
    (Lookback.SEVEN_MONTH, Timeframe.FIFTEEN_MINUTES): 2880 * 7,
    (Lookback.SEVEN_MONTH, Timeframe.ONE_HOUR): 720 * 7,
    (Lookback.EIGHT_MONTH, Timeframe.ONE_MINUTE): 43200 * 8,
    (Lookback.EIGHT_MONTH, Timeframe.FIVE_MINUTES): 8640 * 8,
    (Lookback.EIGHT_MONTH, Timeframe.FIFTEEN_MINUTES): 2880 * 8,
    (Lookback.EIGHT_MONTH, Timeframe.ONE_HOUR): 720 * 8,
    (Lookback.NINE_MONTH, Timeframe.ONE_MINUTE): 43200 * 9,
    (Lookback.NINE_MONTH, Timeframe.FIVE_MINUTES): 8640 * 9,
    (Lookback.NINE_MONTH, Timeframe.FIFTEEN_MINUTES): 2880 * 9,
    (Lookback.NINE_MONTH, Timeframe.ONE_HOUR): 720 * 9,
    (Lookback.TEN_MONTH, Timeframe.ONE_MINUTE): 43200 * 10,
    (Lookback.TEN_MONTH, Timeframe.FIVE_MINUTES): 8640 * 10,
    (Lookback.TEN_MONTH, Timeframe.FIFTEEN_MINUTES): 2880 * 10,
    (Lookback.TEN_MONTH, Timeframe.ONE_HOUR): 720 * 10,
    (Lookback.ELEVEN_MONTH, Timeframe.ONE_MINUTE): 43200 * 11,
    (Lookback.ELEVEN_MONTH, Timeframe.FIVE_MINUTES): 8640 * 11,
    (Lookback.ELEVEN_MONTH, Timeframe.FIFTEEN_MINUTES): 2880 * 11,
    (Lookback.ELEVEN_MONTH, Timeframe.ONE_HOUR): 720 * 11,
    (Lookback.ONE_YEAR, Timeframe.ONE_MINUTE): 43200 * 12,
    (Lookback.ONE_YEAR, Timeframe.FIVE_MINUTES): 8640 * 12,
    (Lookback.ONE_YEAR, Timeframe.FIFTEEN_MINUTES): 2880 * 12,
    (Lookback.ONE_YEAR, Timeframe.ONE_HOUR): 720 * 12,
}
