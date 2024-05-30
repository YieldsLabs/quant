from abc import ABC, abstractmethod
from typing import Tuple

from wasmtime import Engine, Module

Pointer = Tuple[int]


class AbstractWasmService(ABC):
    @abstractmethod
    def get_module(self, identifier: str, engine: Engine) -> Module:
        pass
