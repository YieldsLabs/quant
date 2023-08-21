from enum import Enum

from core.timeframe import Timeframe


class Lookback(Enum):
    ONE_MONTH = '1M'
    THREE_MONTH = '3M'
    SIX_MONTH = '6M'
    ONE_YEAR = '1Y'


TIMEFRAMES_TO_LOOKBACK = {
    (Lookback.ONE_MONTH, Timeframe.ONE_MINUTE): 43200,
    (Lookback.ONE_MONTH, Timeframe.FIVE_MINUTES): 8640,
    (Lookback.ONE_MONTH, Timeframe.FIFTEEN_MINUTES): 2880,

    (Lookback.THREE_MONTH, Timeframe.ONE_MINUTE): 43200 * 3,
    (Lookback.THREE_MONTH, Timeframe.FIVE_MINUTES): 8640 * 3,
    (Lookback.THREE_MONTH, Timeframe.FIFTEEN_MINUTES): 2880 * 3,

    (Lookback.SIX_MONTH, Timeframe.ONE_MINUTE): 43200 * 6,
    (Lookback.SIX_MONTH, Timeframe.FIVE_MINUTES): 8640 * 6,
    (Lookback.SIX_MONTH, Timeframe.FIFTEEN_MINUTES): 2880 * 6,

    (Lookback.ONE_YEAR, Timeframe.ONE_MINUTE): 43200 * 12,
    (Lookback.ONE_YEAR, Timeframe.FIVE_MINUTES): 8640 * 12,
    (Lookback.ONE_YEAR, Timeframe.FIFTEEN_MINUTES): 2880 * 12,
}
