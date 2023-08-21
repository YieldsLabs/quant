from dataclasses import asdict, dataclass


@dataclass
class OHLCV:
    timestamp: int
    open: float
    high: float
    low: float
    close: float
    volume: float

    @classmethod
    def from_raw(cls, data) -> "OHLCV":
        timestamp, open, high, low, close, volume = data

        return cls(
            int(timestamp),
            float(open),
            float(high),
            float(low),
            float(close),
            float(volume),
        )

    def to_dict(self):
        return asdict(self)