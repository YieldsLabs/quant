from abc import abstractmethod
from ohlcv.context import ohlcv
from shared.meta_label.abstract_meta_label import AbstractMetaLabel
from shared.meta_label.meta_label import meta_label
from shared.position_side import PositionSide


@ohlcv
@meta_label
class AbstractStopLoss(AbstractMetaLabel):
    SUFFIX = "_STPLSS"
    NAME = ""

    @abstractmethod
    def next(self, position_side: PositionSide, entry_price: float):
        pass
