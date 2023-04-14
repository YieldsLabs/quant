from typing import Final, Optional, Type
import pandas as pd

from ohlcv.abstract_datasource import AbstractDatasource

OHLCV_COLUMNS: Final = ('timestamp', 'open', 'high', 'low', 'close', 'volume')


class OhlcvContext:
    _instance = None
    _datasource = None

    def __new__(cls, datasource: Optional[Type[AbstractDatasource]] = None, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(OhlcvContext, cls).__new__(cls, *args, **kwargs)
            cls._datasource = datasource
        return cls._instance

    def __init__(self, datasource: Optional[Type[AbstractDatasource]] = None):
        if datasource and not self._datasource:
            self._datasource = datasource
        self._ohlcv = pd.DataFrame()

    def update(self, symbol: str, timeframe: str):
        self.ohlcv = self._datasource.fetch(symbol, timeframe)

    @property
    def ohlcv(self) -> pd.DataFrame:
        return self._ohlcv

    @ohlcv.setter
    def ohlcv(self, ohlcv: pd.DataFrame):
        if not set(OHLCV_COLUMNS).issubset(ohlcv.columns):
            raise ValueError(f"The DataFrame must have the following columns: {OHLCV_COLUMNS}")

        self._ohlcv = ohlcv

def ohlcv(cls: Type):
    class Wrapped(cls):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.ohlcv_context = OhlcvContext()

    Wrapped.__name__ = cls.__name__
    Wrapped.__doc__ = cls.__doc__
    return Wrapped


def update_ohlcv(func):
    def wrapper(self, *args, **kwargs):
        _, symbol, timeframe = args
        
        ohlcv_context = OhlcvContext()
        ohlcv_context.update(symbol, timeframe)

        return func(self, *args, **kwargs)

    return wrapper
