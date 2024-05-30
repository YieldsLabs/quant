from wasmtime import Engine, Module

from core.interfaces.abstract_wasm_service import AbstractWasmService
from core.models.wasm_type import WasmType


class WasmFileService(AbstractWasmService):
    _type = {
        WasmType.TREND: "trend_follow.wasm",
        WasmType.TIMESERIES: "timeseries.wasm",
    }

    def __init__(self, dir="wasm"):
        super().__init__()
        self.dir = dir

    def get_module(self, type: WasmType, engine: Engine) -> Module:
        if type not in WasmType:
            raise ValueError(f"Unknown Strategy: {type}")

        wasm_path = f"./{self.dir}/{self._type.get(type)}"

        return Module.from_file(engine, wasm_path)
