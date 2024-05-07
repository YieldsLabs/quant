from dataclasses import asdict, dataclass
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

    def __lt__(self, other: object):
        if not isinstance(other, OHLCV):
            return NotImplemented

        return self.timestamp < other.timestamp

    def __eq__(self, other):
        if not isinstance(other, OHLCV):
            return False

        return self.timestamp == other.timestamp

    def to_dict(self):
        return asdict(self)
