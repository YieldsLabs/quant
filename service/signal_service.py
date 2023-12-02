from ctypes import addressof, c_ubyte
from typing import Optional

from wasmtime import Instance, Linker, Store, WasiConfig

from core.interfaces.abstract_signal_service import AbstractSignalService
from core.interfaces.abstract_wasm_service import AbstractWasmService
from core.models.strategy import Strategy, StrategyType
from core.models.strategy_ref import StrategyRef


class SignalService(AbstractSignalService):
    def __init__(self, wasm_service: AbstractWasmService):
        self.wasm_service = wasm_service
        self.store = Store()
        wasi_config = WasiConfig()
        wasi_config.wasm_multi_value = True
        self.store.set_wasi(wasi_config)
        self.linker = Linker(self.store.engine)
        self.linker.define_wasi()
        self.instance: Optional[Instance] = None

    def _load(self, type: StrategyType):
        module = self.wasm_service.get_module(type, self.store.engine)
        self.instance = self.linker.instantiate(self.store, module)

    def register(self, strategy: Strategy) -> StrategyRef:
        if not self.instance:
            self._load(strategy.type)

        exports = self.instance.exports(self.store)

        data = {
            "signal": strategy.parameters[0],
            "filter": strategy.parameters[1],
            "pulse": strategy.parameters[2],
            "baseline": strategy.parameters[3],
            "stoploss": strategy.parameters[4],
            "exit": strategy.parameters[5],
        }

        allocation_data = {
            key: self._allocate_and_write(self.store, exports, data)
            for key, data in data.items()
        }

        id = exports["register"](
            self.store, *[item for pair in allocation_data.values() for item in pair]
        )

        return StrategyRef(id=id, instance_ref=self.instance, store_ref=self.store)

    @staticmethod
    def _allocate_and_write(store, exports, data: bytes) -> (int, int):
        ptr = exports["allocate"](store, len(data))
        memory = exports["memory"]

        total_memory_size = memory.data_len(store)
        data_ptr = memory.data_ptr(store)
        data_array = (c_ubyte * total_memory_size).from_address(
            addressof(data_ptr.contents)
        )
        data_array[ptr : ptr + len(data)] = data

        return ptr, len(data)
