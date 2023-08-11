import ctypes
from core.events.ohlcv import OHLCV
from  wasmtime import Memory, Store, Linker, WasiConfig, Module

class StrategyActor:
    def __init__(self, linker: Linker, store: Store, module: Module):
        self.store = store
        self.instance = linker.instantiate(self.store, module)
        self.strategy_id = None

    def start(self, strategy, *args):
        self.strategy_id = self.instance.exports(self.store)[f"register_{strategy}"](self.store, *args)

    def stop(self):
        self.instance.exports(self.store)[f"unregister_strategy"](self.store, self.strategy_id)
        self.strategy_id = None

    def next(self, data: OHLCV):
        if self.strategy_id is None:
            raise RuntimeError("Strategy is not started")
        
        strategy_next = self.instance.exports(self.store)["strategy_next"]

        result = strategy_next(self.store, self.strategy_id, data.open, data.high, data.low, data.close, data.volume)

        return result
    
    @property
    def id(self):
        if self.strategy_id is None:
            raise RuntimeError("Strategy is not started")

        exports = self.instance.exports(self.store)
        params = exports["strategy_parameters"](self.store, self.strategy_id)
        memory = exports["memory"]

        return get_string_from_memory(self.store, memory, params[0], params[1])

def get_string_from_memory(store: Store, memory: Memory, pointer, length):
    data_ptr = memory.data_ptr(store)
    data_address = ctypes.addressof(data_ptr.contents)
    final_address = data_address + pointer

    if pointer + length > memory.data_len(store):
        raise ValueError("Pointer and length exceed memory bounds")

    byte_array = (ctypes.c_char * length).from_address(final_address)
    
    return byte_array.value.decode('utf-8')

class StrategyActorFactory:
    def __init__(self):
        self.store = Store()
        self.linker = Linker(self.store.engine)
        wasi_config = WasiConfig()
        self.store.set_wasi(wasi_config)
        self.linker.define_wasi()

    def create_actor(self, wasm_path):
        module = Module.from_file(self.store.engine, wasm_path)
        return StrategyActor(self.linker, self.store, module)