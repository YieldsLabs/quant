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

    def to_dict(self):
        return asdict(self)
