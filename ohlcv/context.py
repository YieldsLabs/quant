from typing import Final, Type
import pandas as pd

from ohlcv.abstract_datasource import AbstractDatasource

OHLCV_COLUMNS: Final = ('timestamp', 'open', 'high', 'low', 'close', 'volume')


class OhlcvContext:
    def __init__(self, datasource: Type[AbstractDatasource]):
        self._ohlcv = pd.DataFrame()
        self.datasource = datasource

    def update(self, symbol: str, timeframe: str):
        self.ohlcv = self.datasource.fetch(symbol, timeframe)

    @property
    def ohlcv(self) -> pd.DataFrame:
        return self._ohlcv.copy()

    @ohlcv.setter
    def ohlcv(self, ohlcv: pd.DataFrame):
        if not set(OHLCV_COLUMNS).issubset(ohlcv.columns):
            raise ValueError(f"The DataFrame must have the following columns: {OHLCV_COLUMNS}")

        self._ohlcv = ohlcv


def ohlcv(cls: Type):
    class Wrapped(cls):
        def __init__(self, ohlcv_context: OhlcvContext, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.ohlcv_context = ohlcv_context

    Wrapped.__name__ = cls.__name__
    Wrapped.__doc__ = cls.__doc__
    return Wrapped


def update_ohlcv(func):
    def wrapper(self, *args, **kwargs):
        _, symbol, timeframe = args
        self.ohlcv_context.update(symbol, timeframe)
        return func(self, *args, **kwargs)

    return wrapper
