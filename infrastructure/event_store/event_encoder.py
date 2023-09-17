from enum import Enum
import json
import numpy as np

from core.interfaces.abstract_position_risk_strategy import AbstractPositionRiskStrategy
from core.interfaces.abstract_position_take_profit_strategy import AbstractPositionTakeProfitStrategy
from core.events.base import Event


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
        
        return super().default(obj)