from typing import Type
import pandas as pd

class OhlcvContext:
    def __init__(self):
        self._ohlcv = pd.DataFrame()

    @property
    def ohlcv(self) -> pd.DataFrame:
        return self._ohlcv.copy()

    @ohlcv.setter
    def ohlcv(self, ohlcv: pd.DataFrame):
        required_columns = ['timestamp', 'open', 'high', 'low', 'close', 'volume']
        
        if not set(required_columns).issubset(ohlcv.columns):
            raise ValueError(f"The DataFrame must have the following columns: {required_columns}")
        
        self._ohlcv = ohlcv

def inject_ohlcv(cls: Type):
    class Wrapped(cls):
        def __init__(self, ohlcv_context: OhlcvContext, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.ohlcv_context = ohlcv_context

    Wrapped.__name__ = cls.__name__
    Wrapped.__doc__ = cls.__doc__
    return Wrapped

def update_ohlcv_data(func):
    def wrapper(self, *args, **kwargs):
        _, symbol, timeframe = args
        self.ohlcv_context.ohlcv = self.broker.get_historical_data(symbol, timeframe, lookback=self.lookback)
        return func(self, *args, **kwargs)
    return wrapper