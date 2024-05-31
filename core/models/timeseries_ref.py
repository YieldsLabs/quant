from dataclasses import dataclass
from typing import Optional

import orjson as json
from wasmtime import Instance, Store

from .ohlcv import OHLCV
from .ta import TechAnalysis


@dataclass(frozen=True)
class TimeSeriesRef:
    id: int
    instance_ref: Instance
    store_ref: Store

    def unregister(self):
        exports = self.instance_ref.exports(self.store_ref)
        exports["timeseries_unregister"](self.store_ref, self.id)
        self.store_ref.gc()

    def add(self, bar: OHLCV):
        exports = self.instance_ref.exports(self.store_ref)

        exports["timeseries_add"](
            self.store_ref,
            self.id,
            bar.timestamp,
            bar.open,
            bar.high,
            bar.low,
            bar.close,
            bar.volume,
        )

    def find_next_bar(self, bar: OHLCV) -> Optional[OHLCV]:
        exports = self.instance_ref.exports(self.store_ref)

        [bar_ptr, bar_len] = exports["timeseries_find_next_bar"](
            self.store_ref,
            self.id,
            bar.timestamp,
            bar.open,
            bar.high,
            bar.low,
            bar.close,
            bar.volume,
        )

        if bar_ptr == -1 and bar_len == 0:
            return None

        buff = exports["memory"].data_ptr(self.store_ref)[bar_ptr : bar_ptr + bar_len]

        try:
            raw_bar = json.loads("".join(chr(val) for val in buff))
            bar = OHLCV.from_list(raw_bar.values())
        except Exception:
            bar = None

        return bar

    def find_prev_bar(self, bar: OHLCV) -> Optional[OHLCV]:
        exports = self.instance_ref.exports(self.store_ref)

        [bar_ptr, bar_len] = exports["timeseries_find_prev_bar"](
            self.store_ref,
            self.id,
            bar.timestamp,
            bar.open,
            bar.high,
            bar.low,
            bar.close,
            bar.volume,
        )

        if bar_ptr == -1 and bar_len == 0:
            return None

        buff = exports["memory"].data_ptr(self.store_ref)[bar_ptr : bar_ptr + bar_len]

        try:
            raw_bar = json.loads("".join(chr(val) for val in buff))
            bar = OHLCV.from_list(raw_bar.values())
        except Exception:
            bar = None

        return bar

    def ta(self, bar: OHLCV) -> Optional[TechAnalysis]:
        exports = self.instance_ref.exports(self.store_ref)

        [bar_ptr, bar_len] = exports["timeseries_ta"](
            self.store_ref,
            self.id,
            bar.timestamp,
            bar.open,
            bar.high,
            bar.low,
            bar.close,
            bar.volume,
        )

        if bar_ptr == -1 and bar_len == 0:
            return None

        buff = exports["memory"].data_ptr(self.store_ref)[bar_ptr : bar_ptr + bar_len]

        try:
            raw_ta = json.loads("".join(chr(val) for val in buff))
            ta = TechAnalysis.from_list(raw_ta.values())
        except Exception:
            ta = None

        return ta
