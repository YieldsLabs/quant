import json
from dataclasses import fields
from enum import Enum
from typing import Any, Dict, List


class Entity:
    def to_dict(self) -> Dict[str, Any]:
        field_dict = {f.name: getattr(self, f.name) for f in fields(self)}

        property_dict = {
            k: getattr(self, k)
            for k in dir(self)
            if isinstance(getattr(self.__class__, k, None), property)
        }

        result = {**field_dict, **property_dict}

        for key, value in result.items():
            if hasattr(value, "to_dict") and callable(value.to_dict):
                result[key] = value.to_dict()
            elif isinstance(value, Enum):
                result[key] = str(value)
            elif isinstance(value, list):
                result[key] = [
                    v.to_dict() if hasattr(v, "to_dict") and callable(v.to_dict) else v
                    for v in value
                ]

        return result

    def to_json(self) -> str:
        return json.dumps(self.to_dict(), default=str)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Entity":
        return cls(**data)

    @classmethod
    def from_json(cls, json_str: str) -> "Entity":
        return cls.from_dict(json.loads(json_str))

    @classmethod
    def from_list(cls, values: List[Any]) -> "Entity":
        field_names = [f.name for f in fields(cls)]

        if len(values) != len(field_names):
            raise ValueError(f"Expected {len(field_names)} values, got {len(values)}.")

        data = dict(zip(field_names, values))

        return cls.from_dict(data)

    def __str__(self) -> str:
        field_dict = {
            key: value
            for key, value in self.to_dict().items()
            if not key.startswith("_")
        }

        def format_value(value):
            if isinstance(value, dict):
                items = ", ".join(f"{k}={format_value(v)}" for k, v in value.items())
                return f"{{{items}}}"
            elif isinstance(value, list):
                items = ", ".join(format_value(v) for v in value)
                return f"[{items}]"
            elif isinstance(value, float):
                return f"{value:.8f}"
            return str(value)

        return ", ".join(
            f"{key}={format_value(value)}" if value is not None else f"{key}=NA"
            for key, value in field_dict.items()
        )

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self.__str__()})"

    def __format__(self, format_spec: str) -> str:
        return self.to_json() if format_spec == "json" else self.__str__()
