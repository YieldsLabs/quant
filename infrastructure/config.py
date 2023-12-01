from typing import Dict

from core.interfaces.abstract_config import AbstractConfig, ConfigType

DataType = Dict[str, ConfigType]


class ConfigService(AbstractConfig):
    def __init__(self):
        super().__init__()
        self._config: DataType = {}

    def get(self, prop: str) -> ConfigType:
        return self._config.get(prop, None)

    def load(self, config_path: str) -> None:
        self._config: DataType = {}
        current_section = None

        try:
            with open(config_path, "r") as file:
                for line in file:
                    line = line.strip()

                    if line.startswith("[") and line.endswith("]"):
                        current_section = line[1:-1]
                        self._config[current_section] = {}
                    elif current_section is not None and "=" in line:
                        key, value = map(str.strip, line.split("=", 1))
                        if "." in value:
                            try:
                                float_value = float(value)
                                self._config[current_section][key] = (
                                    int(float_value)
                                    if float_value.is_integer()
                                    else float_value
                                )
                            except ValueError:
                                self._config[current_section][key] = value
                        else:
                            try:
                                self._config[current_section][key] = int(value)
                            except ValueError:
                                self._config[current_section][key] = value
        except FileNotFoundError:
            pass

    def update(self, new_config: ConfigType) -> None:
        self._config = self._deep_merge(self._config, new_config)

    def _deep_merge(self, target: ConfigType, source: ConfigType) -> ConfigType:
        for key, value in source.items():
            if (
                isinstance(value, dict)
                and key in target
                and isinstance(target[key], dict)
            ):
                target[key] = self._deep_merge(target[key], value)
            else:
                target[key] = value

        return target
