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
    ONE_YEAR_ONE_MONTH = "1Y1M"
    ONE_YEAR_TWO_MONTH = "1Y2M"
    ONE_YEAR_THREE_MONTH = "1Y3M"
    ONE_YEAR_FOUR_MONTH = "1Y4M"
    ONE_YEAR_FIVE_MONTH = "1Y5M"
    ONE_YEAR_SIX_MONTH = "1Y6M"
    ONE_YEAR_SEVEN_MONTH = "1Y7M"
    ONE_YEAR_EIGHT_MONTH = "1Y8M"
    ONE_YEAR_NINE_MONTH = "1Y9M"
    ONE_YEAR_TEN_MONTH = "1Y10M"
    ONE_YEAR_ELEVEN_MONTH = "1Y11M"
    TWO_YEARS = "2Y"
    TWO_YEARS_ONE_MONTH = "2Y1M"
    TWO_YEARS_TWO_MONTH = "2Y2M"
    TWO_YEARS_THREE_MONTH = "2Y3M"
    TWO_YEARS_FOUR_MONTH = "2Y4M"
    TWO_YEARS_FIVE_MONTH = "2Y5M"
    TWO_YEARS_SIX_MONTH = "2Y6M"
    TWO_YEARS_SEVEN_MONTH = "2Y7M"
    TWO_YEARS_EIGHT_MONTH = "2Y8M"
    TWO_YEARS_NINE_MONTH = "2Y9M"
    TWO_YEARS_TEN_MONTH = "2Y10M"
    TWO_YEARS_ELEVEN_MONTH = "2Y11M"
    THREE_YEARS = "3Y"

    @classmethod
    def from_raw(cls, value: int) -> "Lookback":
        if value < 12:
            formatted_value = f"{value}M"
        else:
            years = value // 12
            months = value % 12
            formatted_value = f"{years}Y" if months == 0 else f"{years}Y{months}M"

        for lookback in cls:
            if lookback.value == formatted_value:
                return lookback

        raise ValueError(f"No matching Lookback for value: {formatted_value}")

    def __str__(self):
        return self.value


TIMEFRAMES_TO_LOOKBACK = {}

for lookback in Lookback:
    for timeframe in Timeframe:
        if lookback == Lookback.ONE_YEAR:
            time_in_months = 12
        elif lookback == Lookback.TWO_YEARS:
            time_in_months = 2 * 12
        else:
            years = 0
            months = 0

            if "Y" in lookback.value:
                idx = lookback.value.index("Y")
                years = int(lookback.value[:idx])

            if "M" in lookback.value:
                idx = lookback.value.index("M")
                months = int(lookback.value[idx - 1])

            time_in_months = years * 12 + months

        if timeframe == Timeframe.ONE_MINUTE:
            time_in_minutes = 43200 * time_in_months
        elif timeframe == Timeframe.FIVE_MINUTES:
            time_in_minutes = 8640 * time_in_months
        elif timeframe == Timeframe.FIFTEEN_MINUTES:
            time_in_minutes = 2880 * time_in_months
        elif timeframe == Timeframe.ONE_HOUR:
            time_in_minutes = 720 * time_in_months

        TIMEFRAMES_TO_LOOKBACK[(lookback, timeframe)] = time_in_minutes
