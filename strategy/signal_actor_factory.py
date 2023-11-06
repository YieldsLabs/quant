from wasmtime import Linker, Module, Store, WasiConfig

from core.interfaces.abstract_signal_actor_factory import AbstractSignalActorFactory
from core.interfaces.abstract_wasm_service import AbstractWasmService

from .signal_actor import SignalActor


class SignalActorFactory(AbstractSignalActorFactory):
    def __init__(self, service: AbstractWasmService):
        super().__init__()
        self.wasm_service = service

    def create_actor(self, symbol, timeframe, strategy):
        store = Store()
        wasi_config = WasiConfig()
        wasi_config.wasm_multi_value = True
        linker = Linker(store.engine)
        store.set_wasi(wasi_config)
        linker.define_wasi()

        wasm_path = self.wasm_service.get_path(strategy.type)
        module = Module.from_file(store.engine, wasm_path)
        instance = linker.instantiate(store, module)
        exports = instance.exports(store)

        return SignalActor(symbol, timeframe, strategy, store, exports)
