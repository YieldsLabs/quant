from dotenv import load_dotenv
import os
import websocket
import json
from broker import Broker, MarginMode, PositionMode
from strategy.AwesomeOscillatorBBStrategy import AwesomeOscillatorBBStrategy
from strategy.ExtremeEuphoriaBBStrategy import ExtremeEuphoriaBBStrategy
from strategy.PSARZeroLagEMAStrategy import PSARZeroLagEMAStrategy
from strategy.SwingIndicatorStrategy import SwingIndicatorStrategy
from trader import Trader

from risk_management.riskmanager import RiskManager
from risk_management.stop_loss import ATRStopLossFinder, LowHighStopLossFinder, SimpleStopLossFinder, TrailingStopLossFinder
from risk_management.take_profit import EmptyTakeProfitFinder, RiskRewardTakeProfitFinder, SimpleTakeProfitFinder

from strategy.EngulfingSMA import EngulfingSMA
from strategy.BollingerEngulfing import BollingerEngulfing

load_dotenv()

symbol = 'LPTUSDT'
timeframe = '1'
leverage = 1
channels = [f"kline.{timeframe}.{symbol}"]

API_KEY = os.getenv('API_KEY')
API_SECRET = os.getenv('API_SECRET')

atr_multi = 1.2
risk_reward_ratio = 1.5
risk_per_trade = 0.0001
stop_loss_pct = 0.002
lookback_period = 30

broker = Broker(API_KEY, API_SECRET)
broker.set_leverage(symbol, leverage)
broker.set_position_mode(symbol, PositionMode.ONE_WAY)
broker.set_margin_mode(symbol, mode=MarginMode.ISOLATED, leverage=leverage)

ohlcv = broker.get_historical_data(symbol, f"{timeframe}m")
stop_loss_finder = ATRStopLossFinder(multiplier=atr_multi)
#stop_loss_finder = TrailingStopLossFinder()
take_profit_finder = RiskRewardTakeProfitFinder(risk_reward_ratio=risk_reward_ratio)
#take_profit_finder = EmptyTakeProfitFinder()
rm = RiskManager(stop_loss_finder, take_profit_finder, risk_per_trade=risk_per_trade)
strategy = EngulfingSMA()
trader = Trader(broker, rm)

def on_open(ws):
    print("WebSocket connection opened")
    for channel in channels:
        ws.send(json.dumps({"op": "subscribe", "args": [channel]}))


def on_message(ws, message):
    trader.trade(strategy, symbol, f"{timeframe}m")

def on_error(ws, error):
    print(f"WebSocket error: {error}")


def on_close(ws):
    print("WebSocket connection closed")


ws = websocket.WebSocketApp(
    'wss://stream.bybit.com/v5/public/linear',
    on_open=on_open,
    on_message=on_message,
    on_error=on_error,
    on_close=on_close
)

ws.run_forever()
