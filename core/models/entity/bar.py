from ._base import Entity
from .ohlcv import OHLCV


@Entity
class Bar:
    ohlcv: OHLCV
    closed: bool
