from dotenv import load_dotenv
import os
import websocket
import json
from analytics.performance import PerformanceStats
from broker.futures_bybit_broker import FuturesBybitBroker
from broker.margin_mode import MarginMode
from broker.position_mode import PositionMode
from ohlcv.bybit_datasource import BybitDataSource
from ohlcv.context import OhlcvContext
from risk_management.stop_loss.base.atr_stop_loss_finder import ATRStopLossFinder
from risk_management.take_profit.risk_reward_take_profit_finder import RiskRewardTakeProfitFinder

from risk_management.risk_manager import RiskManager
from shared.timeframes import Timeframes
from strategy.extreme_euphoria_bb_strategy import ExtremeEuphoriaBBStrategy
from trader.simple_trader import SimpleTrader

load_dotenv()

API_KEY = os.getenv('API_KEY')
API_SECRET = os.getenv('API_SECRET')

symbol = 'SOLUSDT'
timeframe = Timeframes.ONE_MINUTE
leverage = 1
atr_multi = 0.85
risk_reward_ratio = 1.5
risk_per_trade = 0.00001
lookback_period = 20
slow_sma_period = 100
lookback = 1000

broker = FuturesBybitBroker(API_KEY, API_SECRET)
broker.set_leverage(symbol, leverage)
broker.set_position_mode(symbol, position_mode=PositionMode.ONE_WAY)
broker.set_margin_mode(symbol, margin_mode=MarginMode.ISOLATED, leverage=leverage)

market = broker.get_symbol_info(symbol)
initial_balance = broker.get_account_balance()

datasource = BybitDataSource(broker, lookback)
ohlcv_context = OhlcvContext(datasource)

stop_loss_finder = ATRStopLossFinder(ohlcv_context, multiplier=atr_multi)
take_profit_finder = RiskRewardTakeProfitFinder(risk_reward_ratio=risk_reward_ratio)

rm = RiskManager(stop_loss_finder, take_profit_finder, risk_per_trade=risk_per_trade, **market)
analytics = PerformanceStats(initial_balance)
trader = SimpleTrader(ohlcv_context, broker, rm, analytics)
strategy = ExtremeEuphoriaBBStrategy()


invervals = {
    Timeframes.ONE_MINUTE: 1,
    Timeframes.THREE_MINUTES: 3,
    Timeframes.FIVE_MINUTES: 5,
    Timeframes.FIFTEEN_MINUTES: 15,
    Timeframes.ONE_HOUR: 60,
    Timeframes.FOUR_HOURS: 240,
}

channels = [f"kline.{invervals[Timeframes.ONE_MINUTE]}.{symbol}"]


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
