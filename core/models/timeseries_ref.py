import typing
from dataclasses import dataclass
from typing import Any, Optional

import orjson as json

if typing.TYPE_CHECKING:
    from wasmtime import Instance, Store

from .ohlcv import OHLCV
from .ta import TechAnalysis


@dataclass(frozen=True)
class TimeSeriesRef:
    id: int
    instance_ref: "Instance"
    store_ref: "Store"

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

    def next_bar(self, bar: OHLCV) -> Optional[OHLCV]:
        return self._get_bar("next_bar", bar)

    def prev_bar(self, bar: OHLCV) -> Optional[OHLCV]:
        return self._get_bar("prev_bar", bar)

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

        return self._deserialize(TechAnalysis, bar_ptr, bar_len)

    def _get_bar(self, method: str, bar: "OHLCV") -> Optional["OHLCV"]:
        exports = self.instance_ref.exports(self.store_ref)
        bar_ptr, bar_len = exports[f"timeseries_{method}"](
            self.store_ref,
            self.id,
            bar.timestamp,
            bar.open,
            bar.high,
            bar.low,
            bar.close,
            bar.volume,
        )

        return self._deserialize(OHLCV, bar_ptr, bar_len)

    def _deserialize(self, data_class: Any, ptr: int, length: int) -> Optional[Any]:
        if ptr == -1 and length == 0:
            return None

        exports = self.instance_ref.exports(self.store_ref)
        buff = exports["memory"].data_ptr(self.store_ref)[ptr : ptr + length]

        try:
            raw_data = json.loads("".join(chr(val) for val in buff))
            deserialized_data = data_class.from_list(raw_data.values())
        except Exception:
            deserialized_data = None

        return deserialized_data
