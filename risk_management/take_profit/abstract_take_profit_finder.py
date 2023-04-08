from abc import abstractmethod
from shared.meta_label.abstract_meta_label import AbstractMetaLabel
from shared.meta_label.meta_label import meta_label

from shared.position_side import PositionSide


@meta_label
class AbstractTakeProfit(AbstractMetaLabel):
    SUFFIX = "_TAKEPROFIT"
    NAME = ""

    @abstractmethod
    def next(self, position_side: PositionSide, entry_price: float, stop_loss_price: float):
        pass
