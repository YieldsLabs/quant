from typing import Any, Dict, List

from core.models.candle_type import CandleType

from ._base import Entity


@Entity
class OHLCV:
    timestamp: int
    open: float
    high: float
    low: float
    close: float
    volume: float

    def __post_init__(self):
        if not (
            self.low <= self.open <= self.high and self.low <= self.close <= self.high
        ):
            raise ValueError(
                "Open and Close prices must be between Low and High prices"
            )
        if self.low > self.high:
            raise ValueError("Low price cannot be higher than High price")

    @classmethod
    def from_list(cls, data: List[Any]) -> "OHLCV":
        timestamp, open, high, low, close, volume = data

        return cls(
            int(timestamp),
            float(open),
            float(high),
            float(low),
            float(close),
            float(volume),
        )

    @classmethod
    def from_dict(cls, data: Dict) -> "OHLCV":
        required_keys = {
            "start",
            "timestamp",
            "open",
            "high",
            "low",
            "close",
            "volume",
            "confirm",
        }

        missing_keys = required_keys - data.keys()

        if missing_keys:
            raise ValueError(f"Missing keys in data dictionary: {missing_keys}")

        if not isinstance(data.get("confirm"), bool):
            raise ValueError("'confirm' key must be a boolean value.")

        keys_to_use = {
            True: ["start", "open", "high", "low", "close", "volume"],
            False: ["timestamp", "open", "high", "low", "close", "volume"],
        }

        ohlcv_keys = keys_to_use[data["confirm"]]

        return cls.from_list([data[key] for key in ohlcv_keys])

    @property
    def type(self) -> CandleType:
        if self.price_movement > 0:
            return CandleType.BULLISH

        if self.price_movement < 0:
            return CandleType.BEARISH

        return CandleType.NEUTRAL

    def __lt__(self, other: object):
        if not isinstance(other, OHLCV):
            return NotImplemented

        return self.timestamp < other.timestamp

    def __eq__(self, other):
        if not isinstance(other, OHLCV):
            return False

        return (
            self.timestamp == other.timestamp
            and self.open == other.open
            and self.high == other.high
            and self.low == other.low
            and self.close == other.close
            and self.volume == other.volume
        )
