import json
from enum import Enum
from typing import Any

import numpy as np

from core.events.base import Event
from core.interfaces.abstract_position_risk_strategy import AbstractPositionRiskStrategy
from core.interfaces.abstract_position_take_profit_strategy import (
    AbstractPositionTakeProfitStrategy,
)


class Encoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Enum):
            return obj.value
        if isinstance(obj, AbstractPositionRiskStrategy):
            return obj.__class__.__name__
        if isinstance(obj, AbstractPositionTakeProfitStrategy):
            return obj.__class__.__name__
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        if isinstance(obj, Event):
            return obj.to_dict()
        if isinstance(obj, type(Any)):
            return "Any"

        return super().default(obj)
