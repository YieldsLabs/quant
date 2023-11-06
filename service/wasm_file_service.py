from core.interfaces.abstract_wasm_service import AbstractWasmService
from core.models.strategy import StrategyType


class WasmFileService(AbstractWasmService):
    _path_map = {StrategyType.TREND: "trend_follow.wasm"}

    def __init__(self, dir="wasm"):
        super().__init__()
        self.dir = dir

    def get_path(self, type: StrategyType) -> str:
        if type not in StrategyType:
            raise ValueError(f"Unknown Strategy: {type}")

        return f"./{self.dir}/{self._path_map.get(type)}"
