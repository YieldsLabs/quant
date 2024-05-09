from abc import ABC, abstractmethod

from core.models.strategy import Strategy
from core.models.strategy_ref import StrategyRef
from core.models.wasm_type import WasmType


class AbstractSignalService(ABC):
    @abstractmethod
    def register(self, strategy: Strategy, wasm: WasmType) -> StrategyRef:
        pass
