from dataclasses import dataclass

from core.models.ohlcv import OHLCV


@dataclass(frozen=True)
class Bar:
    ohlcv: OHLCV
    closed: bool
