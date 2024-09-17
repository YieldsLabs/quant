from dataclasses import asdict, dataclass, fields
from enum import Enum
from typing import Any


@dataclass(frozen=True)
class Indicator:
    type: Any

    def to_dict(self) -> dict:
        d = asdict(self)

        for field in fields(self):
            name = field.name
            value = d[name]

            if isinstance(value, dict) and "_value" in value:
                v = value["_value"]

                if isinstance(v, Enum):
                    d[name] = v.value
                else:
                    d[name] = value["_value"]
            elif isinstance(value, Enum):
                d[name] = value.value

        return d
