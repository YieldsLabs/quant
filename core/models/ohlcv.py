from dataclasses import dataclass
from typing import Any, Dict, List


@dataclass(frozen=True)
class OHLCV:
    timestamp: int
    open: float
    high: float
    low: float
    close: float
    volume: float

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
        return cls.from_list(
            [
                data[key]
                for key in ["timestamp", "open", "high", "low", "close", "volume"]
            ]
        )

    @property
    def real_body(self) -> float:
        return abs(self.open - self.close)

    @property
    def upper_shadow(self) -> float:
        return self.high - max(self.open, self.close)

    @property
    def lower_shadow(self) -> float:
        return min(self.open, self.close) - self.low

    def __lt__(self, other: object):
        if not isinstance(other, OHLCV):
            return NotImplemented

        return self.timestamp < other.timestamp

    def __eq__(self, other):
        if not isinstance(other, OHLCV):
            return False

        return self.timestamp == other.timestamp

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
            "lower_shadow": self.lower_shadow
        }

    def __str__(self):
        return (f"OHLCV(timestamp={self.timestamp}, open={self.open}, high={self.high}, "
                f"low={self.low}, close={self.close}, volume={self.volume}, "
                f"real_body={round(self.real_body, 5)}, "
                f"upper_shadow={round(self.upper_shadow, 5)}, "
                f"lower_shadow={round(self.lower_shadow, 5)})")
