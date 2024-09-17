from dataclasses import dataclass

from .base import Entity
from .ohlcv import OHLCV


@dataclass(frozen=True)
class Bar(Entity):
    ohlcv: OHLCV
    closed: bool
