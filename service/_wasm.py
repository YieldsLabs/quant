from wasmtime import Engine, Linker, Module, Store, WasiConfig

from core.interfaces.abstract_wasm_manager import AbstractWasmManager
from core.models.wasm_type import WasmType


class WasmManager(AbstractWasmManager):
    _type = {
        WasmType.TREND: "trend_follow.wasm",
        WasmType.TIMESERIES: "timeseries.wasm",
    }

    def __init__(self, dir="wasm"):
        super().__init__()
        self.dir = dir
        self.instances = {}

    def load_instance(self, wasm_type: WasmType):
        if wasm_type not in self.instances:
            store = Store()
            self._configure_wasi(store)
            linker = Linker(store.engine)
            linker.define_wasi()
            module = self._get_module(wasm_type, store.engine)
            instance = linker.instantiate(store, module)
            self.instances[wasm_type] = (instance, store)

    def get_instance(self, wasm_type: WasmType):
        self.load_instance(wasm_type)
        return self.instances[wasm_type]

    def _configure_wasi(self, store: Store):
        wasi_config = WasiConfig()
        wasi_config.wasm_multi_value = True
        wasi_config.inherit_stdout()
        store.set_wasi(wasi_config)

    def _get_module(self, type: WasmType, engine: Engine) -> Module:
        if type not in WasmType:
            raise ValueError(f"Unknown Strategy: {type}")

        wasm_path = f"./{self.dir}/{self._type.get(type)}"

        return Module.from_file(engine, wasm_path)
