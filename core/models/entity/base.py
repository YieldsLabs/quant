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
            if isinstance(value, Enum):
                result[key] = str(value)

            elif hasattr(value, "to_dict") and callable(value.to_dict):
                result[key] = value.to_dict()

            elif isinstance(value, list):
                result[key] = [
                    v.to_dict() if hasattr(v, "to_dict") and callable(v.to_dict) else v
                    for v in value
                ]

        return result

    def to_json(self) -> str:
        return json.dumps(self.to_dict())

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Entity":
        return cls(**data)

    @classmethod
    def from_json(cls, json_str: str) -> "Entity":
        data = json.loads(json_str)
        return cls.from_dict(data)

    @classmethod
    def from_list(cls, values: List[Any]) -> "Entity":
        field_names = [f.name for f in fields(cls)]

        if len(values) != len(field_names):
            raise ValueError(f"Expected {len(field_names)} values, got {len(values)}.")

        data = dict(zip(field_names, values))

        return cls.from_dict(data)

    def __str__(self) -> str:
        field_dict = self.to_dict()
        field_strings = []

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

        for key, value in field_dict.items():
            if value is not None:
                formatted_value = format_value(value)
                field_strings.append(f"{key}={formatted_value}")
            else:
                field_strings.append(f"{key}=NA")

        return ", ".join(field_strings)

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self.__str__()})"

    def __format__(self, format_spec: str) -> str:
        if format_spec == "":
            return self.__str__()

        if format_spec == "json":
            return self.to_json()

        return self.__str__()
