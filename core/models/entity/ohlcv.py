from dataclasses import dataclass
from typing import Any, Dict, List

from core.models.candle_type import CandleType

from .base import Entity


@dataclass(frozen=True)
class OHLCV(Entity):
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
        keys = [
            "start",
            "timestamp",
            "open",
            "high",
            "low",
            "close",
            "volume",
            "confirm",
        ]

        if any(key not in data for key in keys):
            raise ValueError(f"Data dictionary must contain the keys: {keys}")

        confirmed = ["start", "open", "high", "low", "close", "volume"]
        not_confirmed = ["timestamp", "open", "high", "low", "close", "volume"]

        ohlcv_keys = not_confirmed if not data["confirm"] else confirmed

        return cls.from_list([data[key] for key in ohlcv_keys])

    @property
    def real_body(self) -> float:
        return abs(self.open - self.close)

    @property
    def upper_shadow(self) -> float:
        return self.high - max(self.open, self.close)

    @property
    def lower_shadow(self) -> float:
        return min(self.open, self.close) - self.low

    @property
    def price_range(self) -> float:
        return self.high - self.low

    @property
    def price_movement(self) -> float:
        return self.close - self.open

    @property
    def body_range_ratio(self) -> float:
        return self.real_body / self.price_range if self.price_range != 0 else 0

    @property
    def body_shadow_ratio(self) -> float:
        total_shadow = self.upper_shadow + self.lower_shadow
        return self.real_body / total_shadow if total_shadow != 0 else 0

    @property
    def shadow_range_ratio(self) -> float:
        total_shadow = self.upper_shadow + self.lower_shadow
        return total_shadow / self.price_range if self.price_range != 0 else 0

    @property
    def real_body_normalized(self) -> float:
        return self.real_body / self.price_range if self.price_range != 0 else 0

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
