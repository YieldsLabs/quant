from abc import ABC, abstractmethod

from wasmtime import Engine, Module


class AbstractWasmService(ABC):
    @abstractmethod
    def get_module(self, identifier: str, engine: Engine) -> Module:
        pass
