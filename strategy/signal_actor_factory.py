from wasmtime import Linker, Store, WasiConfig

from core.interfaces.abstract_signal_actor_factory import AbstractSignalActorFactory
from core.interfaces.abstract_wasm_service import AbstractWasmService

from .signal_actor import SignalActor


class SignalActorFactory(AbstractSignalActorFactory):
    def __init__(self, service: AbstractWasmService):
        super().__init__()
        self.wasm_service = service

    def create_actor(self, symbol, timeframe, strategy):
        store = Store()
        engine = store.engine
        wasi_config = WasiConfig()
        wasi_config.wasm_multi_value = True
        linker = Linker(engine)
        store.set_wasi(wasi_config)
        linker.define_wasi()

        module = self.wasm_service.get_module(strategy.type, engine)
        instance = linker.instantiate(store, module)
        exports = instance.exports(store)

        return SignalActor(symbol, timeframe, strategy, store, exports)
