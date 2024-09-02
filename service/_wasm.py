import os
from functools import lru_cache

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

    @lru_cache(maxsize=None)
    def get_instance(self, wasm_type: WasmType):
        return self._load_instance(wasm_type)

    def _load_instance(self, wasm_type: WasmType):
        store = Store()

        wasi = self._configure_wasi()

        store.set_wasi(wasi)

        linker = self._configure_linker(store.engine)

        module = self._get_module(wasm_type, store.engine)
        instance = linker.instantiate(store, module)

        return (instance, store)

    def _configure_wasi(self) -> WasiConfig:
        wasi_config = WasiConfig()
        wasi_config.wasm_multi_value = True
        wasi_config.inherit_stdout()
        return wasi_config

    def _configure_linker(self, engine: Engine) -> Linker:
        linker = Linker(engine)
        linker.define_wasi()
        return linker

    def _get_module(self, type: WasmType, engine: Engine) -> Module:
        if type not in WasmType:
            raise ValueError(f"Unknown Strategy: {type}")

        wasm_path = f"./{self.dir}/{self._type.get(type)}"

        if not os.path.exists(wasm_path):
            raise FileNotFoundError(f"WASM file not found: {wasm_path}")

        return Module.from_file(engine, wasm_path)
