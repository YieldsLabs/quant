import asyncio
import json
from dotenv import load_dotenv
import os
import websockets
from analytics.strategy_performance import StrategyPerformance
from broker.futures_bybit_broker import FuturesBybitBroker
from datasource.bybit_datasource import BybitDataSource
from journal.log_journal import LogJournal
from optimization.hyperparameters import strategy_hyperparameters, stoploss_hyperparameters, takeprofit_hyperparameters
from core.timeframe import Timeframe
from system.trading_system import TradingSystem

load_dotenv()

API_KEY = os.getenv('API_KEY')
API_SECRET = os.getenv('API_SECRET')
WSS = os.getenv('WSS')

symbols = [
    'ETHUSDT',
    'NEARUSDT',
    'SOLUSDT',
    'AVAXUSDT',
    'XRPUSDT'
]

timeframes = [
    Timeframe.ONE_MINUTE,
    Timeframe.THREE_MINUTES,
    Timeframe.FIVE_MINUTES
]

search_space = {
    **strategy_hyperparameters,
    **stoploss_hyperparameters,
    **takeprofit_hyperparameters
}

lookback = 15000
risk_per_trade = 0.0001

async def process_messages(ws, bybit_trading_system):
    while True:
        try:
            message = await ws.recv()
            message_data = json.loads(message)

            if "topic" in message_data:
                await bybit_trading_system.on_new_candle(message_data)

        except websockets.exceptions.ConnectionClosed as e:
            print(f"Websocket closed with code {e.code}: {e.reason}")
            bybit_trading_system.unsubscibe_candle_stream()
            break
        except Exception as e:
            print(f"Unexpected error: {e}")
            bybit_trading_system.unsubscibe_candle_stream()

async def send_ping(ws, interval):
    while True:
        await asyncio.sleep(interval)
        await ws.ping()

async def main():
    LogJournal()

    broker = FuturesBybitBroker(API_KEY, API_SECRET)
    analytics = StrategyPerformance(risk_per_trade)
    datasource = BybitDataSource(broker)
    bybit_trading_system = TradingSystem(datasource, broker, analytics, symbols, timeframes, lookback=lookback, risk_per_trade=risk_per_trade)
    
    async with websockets.connect(WSS) as ws:
        bybit_trading_system.subscribe_candle_stream(ws)
        
        start_trading_system_task = asyncio.create_task(bybit_trading_system.start())
        ping_task = asyncio.create_task(send_ping(ws, interval=30))
        message_processing_task = asyncio.create_task(process_messages(ws, bybit_trading_system))

        try:
            await asyncio.gather(start_trading_system_task, ping_task, message_processing_task)
        finally:
            ping_task.cancel()
            message_processing_task.cancel()
            start_trading_system_task.cancel()
    
    await asyncio.sleep(0.01)

asyncio.run(main())