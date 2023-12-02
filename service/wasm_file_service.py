from wasmtime import Engine, Module

from core.interfaces.abstract_wasm_service import AbstractWasmService
from core.models.strategy import StrategyType


class WasmFileService(AbstractWasmService):
    _path_map = {StrategyType.TREND: "trend_follow.wasm"}

    def __init__(self, dir="wasm"):
        super().__init__()
        self.dir = dir

    def get_module(self, type: StrategyType, engine: Engine) -> Module:
        if type not in StrategyType:
            raise ValueError(f"Unknown Strategy: {type}")

        wasm_path = f"./{self.dir}/{self._path_map.get(type)}"

        return Module.from_file(engine, wasm_path)
