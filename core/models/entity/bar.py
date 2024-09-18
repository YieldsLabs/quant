from dataclasses import dataclass

from ._base import Entity
from .ohlcv import OHLCV


@dataclass(frozen=True)
class Bar(Entity):
    ohlcv: OHLCV
    closed: bool
