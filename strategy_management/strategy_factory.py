from wasmtime import Store, Linker, WasiConfig, Module

from .abstract_strategy_factory import AbsctractStrategyActorFactory
from .strategy_actor import StrategyActor


class StrategyActorFactory(AbsctractStrategyActorFactory):
    def __init__(self):
        self.store = Store()
        self.linker = Linker(self.store.engine)
        wasi_config = WasiConfig()
        wasi_config.wasm_multi_value = True
        self.store.set_wasi(wasi_config)
        self.linker.define_wasi()

    def create_actor(self, wasm_path, strategy, parameters):
        module = Module.from_file(self.store.engine, wasm_path)

        return StrategyActor(strategy, parameters, self.linker, self.store, module)
