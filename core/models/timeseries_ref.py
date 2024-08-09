import typing
from dataclasses import dataclass
from functools import cached_property
from typing import Any, List, Optional

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

    @cached_property
    def exports(self):
        return self.instance_ref.exports(self.store_ref)

    def unregister(self):
        self.exports["timeseries_unregister"](self.store_ref, self.id)
        self.store_ref.gc()

    def add(self, bar: OHLCV):
        [res, _] = self.exports["timeseries_add"](
            self.store_ref,
            self.id,
            bar.timestamp,
            bar.open,
            bar.high,
            bar.low,
            bar.close,
            bar.volume,
        )

        if res == -1:
            raise ValueError("Can't add new market bar")

    def next_bar(self, bar: OHLCV) -> Optional[OHLCV]:
        return self._get_bar("next_bar", bar)

    def prev_bar(self, bar: OHLCV) -> Optional[OHLCV]:
        return self._get_bar("prev_bar", bar)

    def back_n_bars(self, bar: OHLCV, n: int) -> List[OHLCV]:
        ptr, length = self.exports["timeseries_back_n_bars"](
            self.store_ref,
            self.id,
            bar.timestamp,
            bar.open,
            bar.high,
            bar.low,
            bar.close,
            bar.volume,
            n,
        )

        if ptr == -1 and length == 0:
            return []

        buff = self.exports["memory"].data_ptr(self.store_ref)[ptr : ptr + length]

        try:
            raw_data = json.loads("".join(chr(val) for val in buff))
            deserialized_data = [OHLCV.from_list(d.values()) for d in raw_data]
        except Exception:
            deserialized_data = []

        return deserialized_data

    def ta(self, bar: OHLCV) -> Optional[TechAnalysis]:
        [bar_ptr, bar_len] = self.exports["timeseries_ta"](
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
        bar_ptr, bar_len = self.exports[f"timeseries_{method}"](
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

        buff = self.exports["memory"].data_ptr(self.store_ref)[ptr : ptr + length]

        try:
            raw_data = json.loads("".join(chr(val) for val in buff))
            deserialized_data = data_class.from_list(raw_data.values())
        except Exception:
            deserialized_data = None

        return deserialized_data
