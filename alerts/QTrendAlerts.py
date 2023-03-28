import pandas as pd
from ta.volatility import AverageTrueRange
from enum import Enum

class SignalMode(Enum):
    TypeA = 1
    TypeB = 2

class QTrendAlerts:
    def __init__(self, p=200, atr_p=14, mult=1.0, mode=SignalMode.TypeA, use_ema_smoother=False, src_ema_period=3):
        self.p = p
        self.atr_p = atr_p
        self.mult = mult
        self.mode = mode
        self.use_ema_smoother = use_ema_smoother
        self.src_ema_period = src_ema_period

    def alert(self, ohlcv):
        data = ohlcv.copy()

        if self.use_ema_smoother:
            data['src'] = data['close'].ewm(span=self.src_ema_period).mean()
        else:
            data['src'] = data['close']

        data['h'] = data['src'].rolling(window=self.p).max()
        data['l'] = data['src'].rolling(window=self.p).min()
        data['d'] = data['h'] - data['l']

        atr = AverageTrueRange(data['high'], data['low'], data['close'], self.atr_p).average_true_range()
        data['epsilon'] = self.mult * atr.shift(1)

        if self.mode == SignalMode.TypeA:
            data['change_up'] = data['src'].gt(data['m'] + data['epsilon'])
            data['change_down'] = data['src'].lt(data['m'] - data['epsilon'])
        else:
            data['change_up'] = data['src'] > data['m'] + data['epsilon']
            data['change_down'] = data['src'] < data['m'] - data['epsilon']

        data['sb'] = data['open'].lt(data['l'] + data['d'] / 8) & data['open'].ge(data['l'])
        data['ss'] = data['open'].gt(data['h'] - data['d'] / 8) & data['open'].le(data['h'])
        data['strong_buy'] = data['sb'] | data['sb'].shift(1) | data['sb'].shift(2) | data['sb'].shift(3) | data['sb'].shift(4)
        data['strong_sell'] = data['ss'] | data['ss'].shift(1) | data['ss'].shift(2) | data['ss'].shift(3) | data['ss'].shift(4)

        data['m'] = (data['h'] + data['l']) / 2
        data['m'] = data['m'].where((data['change_up'] | data['change_down']) & (data['m'] != data['m'].shift(1)),
                                    data['m'] + data['epsilon'].where(data['change_up'], data['m'] - data['epsilon']))
        data['m'].fillna(method='ffill', inplace=True)

        buy = (data['change_up'] & ~data['strong_buy'])
        sell = (data['change_down'] & ~data['strong_sell'])

        return buy, sell
