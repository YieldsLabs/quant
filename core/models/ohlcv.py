from dataclasses import dataclass
from enum import Enum, auto
from typing import Any, Dict, List


class CandleType(Enum):
    bullish = auto()
    bearish = auto()
    neutral = auto()

    def __str__(self):
        return self.name.upper()


@dataclass(frozen=True)
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
        keys = ["timestamp", "open", "high", "low", "close", "volume"]

        if any(key not in data for key in keys):
            raise ValueError(f"Data dictionary must contain the keys: {keys}")

        return cls.from_list([data[key] for key in keys])

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
    def type(self) -> CandleType:
        if self.close > self.open:
            return CandleType.bullish
        elif self.close < self.open:
            return CandleType.bearish
        else:
            return CandleType.neutral

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

    def to_dict(self):
        return {
            "timestamp": self.timestamp,
            "open": self.open,
            "high": self.high,
            "low": self.low,
            "close": self.close,
            "volume": self.volume,
            "real_body": self.real_body,
            "upper_shadow": self.upper_shadow,
            "lower_shadow": self.lower_shadow,
            "type": str(self.type),
        }

    def __str__(self) -> str:
        return (
            f"timestamp={self.timestamp}, "
            f"open={self.open}, "
            f"high={self.high}, "
            f"low={self.low}, "
            f"close={self.close}, "
            f"volume={self.volume}, "
            f"real_body={self.real_body:.8f}, "
            f"upper_shadow={self.upper_shadow:.8f}, "
            f"lower_shadow={self.lower_shadow:.8f}, "
            f"type={self.type}"
        )

    def __repr__(self) -> str:
        return (
            f"OHLCV(timestamp={self.timestamp}, "
            f"open={self.open}, "
            f"high={self.high}, "
            f"low={self.low}, "
            f"close={self.close}, "
            f"volume={self.volume}, "
            f"real_body={self.real_body:.8f}, "
            f"upper_shadow={self.upper_shadow:.8f}, "
            f"lower_shadow={self.lower_shadow:.8f}, "
            f"type={self.type})"
        )
