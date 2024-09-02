from abc import ABC, abstractmethod
from typing import Tuple

from wasmtime import Instance, Store

from core.models.wasm_type import WasmType


class AbstractWasmManager(ABC):
    @abstractmethod
    def get_instance(self, wasm_type: WasmType) -> Tuple[Instance, Store]:
        pass
