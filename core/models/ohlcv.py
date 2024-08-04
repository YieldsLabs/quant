from dataclasses import dataclass
from enum import Enum, auto
from typing import Any, Dict, List


class CandleType(Enum):
    BULLISH = auto()
    BEARISH = auto()
    NEUTRAL = auto()

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
            "price_range": self.price_range,
            "price_movement": self.price_movement,
            "body_range_ratio": self.body_range_ratio,
            "body_shadow_ratio": self.body_shadow_ratio,
            "shadow_range_ratio": self.shadow_range_ratio,
            "real_body_normalized": self.real_body_normalized,
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
            f"price_range={self.price_range:.8f}, "
            f"price_movement={self.price_movement:.8f}, "
            f"body_range_ratio={self.body_range_ratio:.8f}, "
            f"body_shadow_ratio={self.body_shadow_ratio:.8f}, "
            f"shadow_range_ratio={self.shadow_range_ratio:.8f}, "
            f"real_body_normalized={self.real_body_normalized:.8f}, "
            f"type={self.type}"
        )

    def __repr__(self) -> str:
        return f"OHLCV({self})"
