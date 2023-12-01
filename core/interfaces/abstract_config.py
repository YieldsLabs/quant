from abc import ABC, abstractmethod
from typing import Dict, Union

ConfigType = Dict[str, Union[str, float]]

class AbstractConfig(ABC):
    @abstractmethod
    def load(self, path: str) -> None:
        pass

    @abstractmethod
    def get(self, prop: str) -> ConfigType:
        pass

    @abstractmethod
    def update(self, new_config: ConfigType) -> None:
        pass