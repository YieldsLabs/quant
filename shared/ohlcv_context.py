from typing import Type
import pandas as pd

class OhlcvContext:
    def __init__(self):
        self._ohlcv = []

    @property
    def ohlcv(self) -> pd.DataFrame:
        return self._ohlcv.copy()

    @ohlcv.setter
    def ohlcv(self, ohlcv: pd.DataFrame):
        self._ohlcv = ohlcv

def inject_ohlcv(cls: Type):
    class Wrapped(cls):
        def __init__(self, ohlcv_context: OhlcvContext, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.ohlcv_context = ohlcv_context

    Wrapped.__name__ = cls.__name__
    Wrapped.__doc__ = cls.__doc__
    return Wrapped