import re
from dotenv import load_dotenv
import os
import numpy as np
import websocket
import json
from analytics.performance import PerformanceStats
from broker.futures_bybit_broker import FuturesBybitBroker
from broker.margin_mode import MarginMode
from broker.position_mode import PositionMode
from ohlcv.bybit_datasource import BybitDataSource
from ohlcv.context import OhlcvContext
from optimization.hyperparameters import strategy_hyperparameters, stoploss_hyperparameters, takeprofit_hyperparameters
from optimization.strategy_screening import StrategyScreening
from risk_management.stop_loss.base.atr_stop_loss_finder import ATRStopLossFinder
from risk_management.stop_loss.low_high_stop_loss_finder import LowHighStopLossFinder
from risk_management.take_profit.risk_reward_take_profit_finder import RiskRewardTakeProfitFinder

from risk_management.risk_manager import RiskManager
from shared.meta_label.meta_label import extract_numeric_params
from shared.timeframes import Timeframes
from strategy.aobb_strategy import AwesomeOscillatorBBStrategy
from strategy.bollinger_engulfing_strategy import BollingerEngulfing
from strategy.engulfing_zlema_strategy import EngulfingSMA
from strategy.extreme_euphoria_bb_strategy import ExtremeEuphoriaBBStrategy
from strategy.fvg_strategy import FairValueGapStrategy
from strategy.kangaroo_tail_strategy import KangarooTailStrategy
from trader.simple_trader import SimpleTrader

load_dotenv()

API_KEY = os.getenv('API_KEY')
API_SECRET = os.getenv('API_SECRET')

lookback = 1000
leverage = 1
risk_per_trade = 0.00001

broker = FuturesBybitBroker(API_KEY, API_SECRET)
initial_balance = broker.get_account_balance()
analytics = PerformanceStats(initial_balance)
datasource = BybitDataSource(broker, lookback)
ohlcv_context = OhlcvContext(datasource)

symbols = [
    'NEARUSDT',
    'SOLUSDT',
    'AVAXUSDT',
    'XRPUSDT'
]

timeframes = [
    Timeframes.ONE_MINUTE,
    Timeframes.THREE_MINUTES,
    Timeframes.FIVE_MINUTES
]


def create_map(classes):
    map = {}
    for cls in classes:
        name = cls.NAME
        if name is not None:
            map[name] = cls
    return map

def parse_label(label: str):
    pattern = r"([A-Z]+[A-Z\d]+)_(\d+[smhd])_STRATEGY([A-Z]+)([\d:.]+)_STOPLOSS([A-Z]+)([\d:.]+)_TAKEPROFIT([A-Z]+)([\d:.]+)"
    matches = re.match(pattern, label)

    symbol = matches.group(1)
    timeframe = matches.group(2)

    strategy_name = matches.group(3)
    strategy_params = [float(p) if '.' in p else int(p) for p in matches.group(4).split(':')]

    stop_loss_name = matches.group(5)
    stop_loss_params = [float(p) if '.' in p else int(p) for p in matches.group(6).split(':')]

    take_profit_name = matches.group(7)
    take_profit_params = [float(p) if '.' in p else int(p) for p in matches.group(8).split(':')]

    return symbol, timeframe, (strategy_name, strategy_params), (stop_loss_name, stop_loss_params), (take_profit_name, take_profit_params)

strategy = [
    EngulfingSMA,
    BollingerEngulfing,
    ExtremeEuphoriaBBStrategy,
    AwesomeOscillatorBBStrategy
]

strategy_map = create_map(strategy)
stoploss_map = create_map([ATRStopLossFinder, LowHighStopLossFinder])
takeprofit_map = create_map([RiskRewardTakeProfitFinder])
timeframe_map = {
    '1m': Timeframes.ONE_MINUTE,
    '3m': Timeframes.THREE_MINUTES,
    '5m': Timeframes.FIVE_MINUTES
}

stop_loss_finders = [] \
    + [ATRStopLossFinder(ohlcv_context, atr_multi=round(atr_multi, 2)) for atr_multi in np.arange(*stoploss_hyperparameters['atr_multi'])] \
    + [LowHighStopLossFinder(ohlcv_context, atr_multi=round(atr_multi, 2)) for atr_multi in np.arange(*stoploss_hyperparameters['atr_multi'])]

take_profit_finders = [] \
    + [RiskRewardTakeProfitFinder(risk_reward_ratio=round(risk_reward_ratio, 2)) for risk_reward_ratio in np.arange(*takeprofit_hyperparameters['risk_reward_ratio'])]

strategies = [cls() for cls in strategy]

screener = StrategyScreening(
    ohlcv=ohlcv_context,
    broker=broker,
    analytics=analytics,
    symbols=symbols,
    timeframes=timeframes,
    strategies=strategies,
    stop_loss_finders=stop_loss_finders,
    take_profit_finders=take_profit_finders,
)

result = screener.run()

result.to_csv('strategy.csv')

label = str(result.head(1)['id'].iloc[0])

symbol, _timeframe, _strategy, _stop_loss, _take_profit = parse_label(label)

timeframe = timeframe_map[_timeframe]
strategy = strategy_map[_strategy[0]](*_strategy[1])
stop_loss_finder = stoploss_map[_stop_loss[0]](ohlcv_context, *_stop_loss[1])
take_profit_finder = takeprofit_map[_take_profit[0]](*_take_profit[1])

broker.set_leverage(symbol, leverage)
broker.set_position_mode(symbol, position_mode=PositionMode.ONE_WAY)
broker.set_margin_mode(symbol, margin_mode=MarginMode.ISOLATED, leverage=leverage)

market = broker.get_symbol_info(symbol)
rm = RiskManager(stop_loss_finder, take_profit_finder, risk_per_trade=risk_per_trade, **market)

trader = SimpleTrader(ohlcv_context, broker, rm, analytics)

invervals = {
    Timeframes.ONE_MINUTE: 1,
    Timeframes.THREE_MINUTES: 3,
    Timeframes.FIVE_MINUTES: 5,
    Timeframes.FIFTEEN_MINUTES: 15,
    Timeframes.ONE_HOUR: 60,
    Timeframes.FOUR_HOURS: 240,
}

channels = [f"kline.{invervals[timeframe]}.{symbol}"]

def on_open(ws):
    print("WebSocket connection opened")
    for channel in channels:
        ws.send(json.dumps({"op": "subscribe", "args": [channel]}))


def on_message(ws, message):
    trader.trade(strategy, symbol, timeframe)


def on_error(ws, error):
    print(f"WebSocket error: {error}")


def on_close(ws):
    print("WebSocket connection closed")


wss = 'wss://stream.bybit.com/v5/public/linear'

ws = websocket.WebSocketApp(
    wss,
    on_open=on_open,
    on_message=on_message,
    on_error=on_error,
    on_close=on_close
)

ws.run_forever()
