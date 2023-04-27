import asyncio
import json
from dotenv import load_dotenv
import os
import websockets
from analytics.strategy_performance import StrategyPerformance
from broker.futures_bybit_broker import FuturesBybitBroker
from datasource.bybit_datasource import BybitDataSource
from journal.gather_journal import GatherJournal
from journal.log_journal import LogJournal
from optimization.hyperparameters import strategy_hyperparameters, stoploss_hyperparameters, takeprofit_hyperparameters
from core.timeframe import Timeframe
from strategies.aobb_strategy import AwesomeOscillatorBollingerBands
from strategies.bollinger_engulfing_strategy import BollingerBandsEngulfing
from strategies.engulfing_zlema_strategy import EngulfingZLMA
from strategies.extreme_euphoria_bb_strategy import ExtremeEuphoriaBollingerBands
from strategies.fvg_strategy import FairValueGapZLMA
from strategies.kangaroo_tail_strategy import KangarooTailZLMA
from system.trading_system import TradingSystem

load_dotenv()

API_KEY = os.getenv('API_KEY')
API_SECRET = os.getenv('API_SECRET')
WSS = os.getenv('WSS')

symbols = [
    'ADAUSDT',
    'APEUSDT',
    'AVAXUSDT',
    'ETCUSDT',
    'ETHUSDT',
    'MATICUSDT',
    'NEARUSDT',
    'SOLUSDT',
    'UNFIUSDT',
    'XRPUSDT'
]

timeframes = [
    Timeframe.ONE_MINUTE,
    Timeframe.THREE_MINUTES,
    Timeframe.FIVE_MINUTES
]

strategies = [
    AwesomeOscillatorBollingerBands,
    BollingerBandsEngulfing,
    EngulfingZLMA,
    ExtremeEuphoriaBollingerBands,
    FairValueGapZLMA,
    KangarooTailZLMA
]

INTERVALS = {
    Timeframe.ONE_MINUTE: 1,
    Timeframe.THREE_MINUTES: 3,
    Timeframe.FIVE_MINUTES: 5,
    Timeframe.FIFTEEN_MINUTES: 15,
    Timeframe.ONE_HOUR: 60,
    Timeframe.FOUR_HOURS: 240,
}

search_space = {
    **strategy_hyperparameters,
    **stoploss_hyperparameters,
    **takeprofit_hyperparameters
}

backtest_lookback = 130000
risk_per_trade = 0.0001

class WebSocketHandler:
    def __init__(self, url, bybit_trading_system):
        self.url = url
        self.bybit_trading_system = bybit_trading_system

    async def connect_to_websocket(self):
        while True:
            try:
                return await websockets.connect(self.url)
            except Exception as e:
                print(f"Failed to connect to websocket: {e}")
                await asyncio.sleep(5)

    async def process_message(self, message):
        message_data = json.loads(message)

        if "topic" in message_data:
            ohlcv = message_data["data"][0]
            topic = message_data["topic"].split(".")
            symbol, interval = topic[2], topic[1]

            ohlcv_event = self.bybit_trading_system.parse_candle_message(symbol, interval, ohlcv)

            await self.bybit_trading_system.dispatcher.dispatch(ohlcv_event)

    async def send_ping(self, ws, interval):
        while True:
            await asyncio.sleep(interval)
            await ws.ping()

    async def process_messages(self, ws):
        while True:
                try:
                    async for message in ws:
                        await self.process_message(message)
                except websockets.exceptions.ConnectionClosed as e:
                    print(f"Websocket closed with code {e.code}: {e.reason}")
                except Exception as e:
                    print(f"Unexpected error: {e}")

    async def run(self, ws_callback, ping_interval=20):
        ws = await self.connect_to_websocket()
        start_trading_system_task = asyncio.create_task(self.bybit_trading_system.start(lambda t: ws_callback(ws, t)))
        ping_task = asyncio.create_task(self.send_ping(ws, interval=ping_interval))
        message_processing_task = asyncio.create_task(self.process_messages(ws))

        try:
            await asyncio.gather(start_trading_system_task, ping_task, message_processing_task)
        finally:
            ping_task.cancel()
            message_processing_task.cancel()
            start_trading_system_task.cancel()

async def send_ping(ws, interval):
    while True:
        await asyncio.sleep(interval)
        await ws.ping()

async def main():
    LogJournal()
    GatherJournal()

    broker = FuturesBybitBroker(API_KEY, API_SECRET)
    analytics = StrategyPerformance(risk_per_trade)
    datasource = BybitDataSource(broker)
    bybit_trading_system = TradingSystem(
        datasource,
        broker,
        analytics,
        strategies,
        symbols,
        timeframes,
        lookback=backtest_lookback,
        risk_per_trade=risk_per_trade
    )

    ws_handler = WebSocketHandler(WSS, bybit_trading_system)

    async def ws_callback(ws, timeframe_symbols):
        channels = [f"kline.{INTERVALS[timeframe]}.{symbol}" for (timeframe, symbol) in timeframe_symbols]

        for channel in channels:
            await ws.send(json.dumps({"op": "subscribe", "args": [channel]}))

    await ws_handler.run(ws_callback)

asyncio.run(main())
