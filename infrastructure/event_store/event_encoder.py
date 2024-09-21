import asyncio
import json
from abc import ABC
from enum import Enum
from typing import Any

import numpy as np

from core.events._base import Event
from core.models.indicator import Indicator


class Encoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Enum):
            return obj.value
        if isinstance(obj, ABC):
            return obj.__class__.__name__
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        if isinstance(obj, Event):
            return obj.to_dict()
        if isinstance(obj, Indicator):
            return obj.to_dict()
        if isinstance(obj, type(Any)):
            return "Any"
        if isinstance(obj, asyncio.Future):
            return None

        return str(obj)
