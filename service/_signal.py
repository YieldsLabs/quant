from ctypes import addressof, c_ubyte
from typing import Tuple

import orjson as json

from core.interfaces.abstract_signal_service import AbstractSignalService
from core.interfaces.abstract_wasm_manager import AbstractWasmManager
from core.models.strategy import Strategy
from core.models.strategy_ref import StrategyRef
from core.models.wasm_type import WasmType


class SignalService(AbstractSignalService):
    def __init__(self, wasm_manager: AbstractWasmManager):
        super().__init__()
        self._wasm_manager = wasm_manager
        self._wasm = WasmType.TREND

    def register(self, strategy: Strategy) -> StrategyRef:
        instance, store = self._wasm_manager.get_instance(self._wasm)
        exports = instance.exports(store)
        allocation_data = [
            self._write(store, exports, json.dumps(param))
            for param in strategy.parameters
        ]

        id = exports["register"](
            store, *[item for pair in allocation_data for item in pair]
        )

        return StrategyRef(id=id, instance_ref=instance, store_ref=store)

    @staticmethod
    def _write(store, exports, data: bytes) -> Tuple[int]:
        ptr = exports["allocate"](store, len(data))
        memory = exports["memory"]

        total_memory_size = memory.data_len(store)
        data_ptr = memory.data_ptr(store)
        data_array = (c_ubyte * total_memory_size).from_address(
            addressof(data_ptr.contents)
        )
        data_array[ptr : ptr + len(data)] = data

        return ptr, len(data)
