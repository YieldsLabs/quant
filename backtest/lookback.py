from enum import Enum

from core.timeframe import Timeframe


class Lookback(Enum):
    ONE_MONTH = '1M'
    THREE_MONTH = '3M'


TIMEFRAMES_TO_LOOKBACK = {
    (Lookback.ONE_MONTH, Timeframe.ONE_MINUTE): 43200,
    (Lookback.ONE_MONTH, Timeframe.FIVE_MINUTES): 8640,
    (Lookback.ONE_MONTH, Timeframe.FIFTEEN_MINUTES): 2880,

    (Lookback.THREE_MONTH, Timeframe.ONE_MINUTE): 43200 * 3,
    (Lookback.THREE_MONTH, Timeframe.FIVE_MINUTES): 8640 * 3,
    (Lookback.THREE_MONTH, Timeframe.FIFTEEN_MINUTES): 2880 * 3
}
