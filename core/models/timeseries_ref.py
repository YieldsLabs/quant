import typing
from dataclasses import dataclass
from functools import cached_property
from typing import Any, List, Optional, Type

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
        res, _ = self.exports["timeseries_add"](
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

        buff = self._read_from_memory(ptr, length)

        return self._deserialize(buff, OHLCV) or []

    def ta(self, bar: OHLCV) -> Optional[TechAnalysis]:
        ptr, length = self.exports["timeseries_ta"](
            self.store_ref,
            self.id,
            bar.timestamp,
            bar.open,
            bar.high,
            bar.low,
            bar.close,
            bar.volume,
        )

        buff = self._read_from_memory(ptr, length)

        return self._deserialize(buff, TechAnalysis)

    def _get_bar(self, method: str, bar: OHLCV) -> Optional[OHLCV]:
        ptr, length = self.exports[f"timeseries_{method}"](
            self.store_ref,
            self.id,
            bar.timestamp,
            bar.open,
            bar.high,
            bar.low,
            bar.close,
            bar.volume,
        )

        buff = self._read_from_memory(ptr, length)

        return self._deserialize(buff, OHLCV)

    def _read_from_memory(self, ptr: int, length: int) -> bytes:
        if ptr == -1 and length == 0:
            return None

        return self.exports["memory"].data_ptr(self.store_ref)[ptr : ptr + length]

    def _deserialize(self, buff: bytes, data_class: Type[Any]) -> Optional[Any]:
        try:
            raw_data = json.loads("".join(chr(val) for val in buff))

            if isinstance(raw_data, dict):
                return data_class.from_list(raw_data.values())
            elif isinstance(raw_data, list):
                return [data_class.from_list(d.values()) for d in raw_data]
            else:
                raise ValueError("Unexpected data format")

        except Exception:
            return None
