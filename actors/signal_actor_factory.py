from wasmtime import Store, Linker, WasiConfig, Module

from core.interfaces.abstract_signal_actor_factory import AbstractSignalActorFactory

from .signal_actor import SignalActor


class SignalActorFactory(AbstractSignalActorFactory):
    def create_actor(self, symbol, timeframe, wasm_path, strategy, parameters):
        store = Store()
        wasi_config = WasiConfig()
        wasi_config.wasm_multi_value = True
        linker = Linker(store.engine)
        store.set_wasi(wasi_config)
        linker.define_wasi()

        module = Module.from_file(store.engine, wasm_path)
        instance = linker.instantiate(store, module)
        exports = instance.exports(store)

        return SignalActor(symbol, timeframe, strategy, parameters, store, exports)
