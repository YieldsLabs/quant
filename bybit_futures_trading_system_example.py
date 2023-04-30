import asyncio
import json
from dotenv import load_dotenv
import os
import websockets
from analytics.strategy_performance import StrategyPerformance
from broker.futures_bybit_broker import FuturesBybitBroker
from broker.margin_mode import MarginMode
from broker.position_mode import PositionMode
from core.abstract_event_manager import AbstractEventManager
from core.events.ohlcv import OHLCV, OHLCVEvent
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
from strategy.kmeans_inference import KMeansInference
from system.trading_system import TradingContext, TradingSystem

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

TIMEFRAMES = {
    '1': Timeframe.ONE_MINUTE,
    '3': Timeframe.THREE_MINUTES,
    '5': Timeframe.FIVE_MINUTES,
    '15': Timeframe.FIFTEEN_MINUTES,
    '60': Timeframe.ONE_HOUR,
    '240': Timeframe.FOUR_HOURS,
}

search_space = {
    **strategy_hyperparameters,
    **stoploss_hyperparameters,
    **takeprofit_hyperparameters
}

backtest_lookback = 30000
risk_per_trade = 0.0001
leverage = 1


class WebSocketHandler(AbstractEventManager):
    def __init__(self, url):
        self.url = url
        self.ws = None

    async def connect_to_websocket(self):
        while True:
            try:
                return await websockets.connect(self.url)
            except Exception as e:
                print(f"Failed to connect to websocket: {e}")
                await asyncio.sleep(1)

    async def process_message(self, message):
        message_data = json.loads(message)

        if "topic" in message_data:
            ohlcv = message_data["data"][0]
            topic = message_data["topic"].split(".")
            symbol, interval = topic[2], topic[1]

            ohlcv_event = self.parse_candle_message(symbol, interval, ohlcv)

            await self.dispatcher.dispatch(ohlcv_event)

    async def send_ping(self, interval):
        while True:
            await asyncio.sleep(interval)
            await self.ws.ping()

    async def process_messages(self):
        while True:
            try:
                async for message in self.ws:
                    await self.process_message(message)
            except websockets.exceptions.ConnectionClosed as e:
                print(f"Websocket closed with code {e.code}: {e.reason}")
            except Exception as e:
                print(f"Unexpected error: {e}")

    async def run(self, ping_interval=10):
        self.ws = await self.connect_to_websocket()

        ping_task = asyncio.create_task(self.send_ping(interval=ping_interval))
        message_processing_task = asyncio.create_task(self.process_messages())

        try:
            await asyncio.gather(ping_task, message_processing_task)
        finally:
            ping_task.cancel()
            message_processing_task.cancel()

    def parse_candle_message(self, symbol, interval, data):
        ohlcv = OHLCV(
            timestamp=int(data["timestamp"]),
            open=float(data["open"]),
            high=float(data["high"]),
            low=float(data["low"]),
            close=float(data["close"]),
            volume=float(data["volume"]),
        )

        timeframe = TIMEFRAMES[interval]

        return OHLCVEvent(
            symbol=symbol,
            timeframe=timeframe,
            ohlcv=ohlcv
        )


async def subscribe(ws, timeframe_symbols):
    channels = [f"kline.{INTERVALS[timeframe]}.{symbol}" for (timeframe, symbol) in timeframe_symbols]

    for channel in channels:
        await ws.send(json.dumps({"op": "subscribe", "args": [channel]}))


async def main():
    LogJournal()
    GatherJournal()

    broker = FuturesBybitBroker(API_KEY, API_SECRET)

    for symbol in symbols:
        broker.set_leverage(symbol, leverage)
        broker.set_position_mode(symbol, position_mode=PositionMode.ONE_WAY)
        broker.set_margin_mode(symbol, margin_mode=MarginMode.ISOLATED, leverage=leverage)

    analytics = StrategyPerformance(risk_per_trade)
    datasource = BybitDataSource(broker)
    inference = KMeansInference('./strategy/model/kmeans_model.pkl', './strategy/model/scaler.pkl')
    ws_handler = WebSocketHandler(WSS)

    context = TradingContext(
        datasource,
        broker,
        analytics,
        inference,
        strategies,
        symbols,
        timeframes,
        lookback=backtest_lookback,
        risk_per_trade=risk_per_trade,
        subscribe=lambda t: subscribe(ws_handler.ws, t)
    )

    bybit_trading_system = TradingSystem(context)

    system_task = asyncio.create_task(bybit_trading_system.start())
    ws_handler_task = asyncio.create_task(ws_handler.run())

    try:
        await asyncio.gather(system_task, ws_handler_task)
    finally:
        system_task.cancel()
        ws_handler_task.cancel()

asyncio.run(main())
