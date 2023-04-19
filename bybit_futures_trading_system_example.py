import asyncio
from dotenv import load_dotenv
import os
import websockets
from analytics.strategy_performance import StrategyPerformance
from broker.futures_bybit_broker import FuturesBybitBroker
from datasource.bybit_datasource import BybitDataSource
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

strategies = [
    AwesomeOscillatorBollingerBands,
    BollingerBandsEngulfing,
    EngulfingZLMA,
    ExtremeEuphoriaBollingerBands,
    FairValueGapZLMA,
    KangarooTailZLMA
]

search_space = {
    **strategy_hyperparameters,
    **stoploss_hyperparameters,
    **takeprofit_hyperparameters
}

lookback = 800
risk_per_trade = 0.001

async def process_messages(ws, bybit_trading_system):
    while True:
        try:
            message = await ws.recv()
            bybit_trading_system.on_new_candle(message)
        except websockets.exceptions.ConnectionClosed as e:
            print(f"Websocket closed with code {e.code}: {e.reason}")
            bybit_trading_system.unsubscibe_candle_stream()
            break
        except Exception as e:
            print(f"Unexpected error: {e}")
            bybit_trading_system.unsubscibe_candle_stream()

async def main():
    while True:
        LogJournal()
        
        broker = FuturesBybitBroker(API_KEY, API_SECRET)
        datasource = BybitDataSource(broker)
        analytics = StrategyPerformance(datasource, risk_per_trade)
        bybit_trading_system = TradingSystem(datasource, broker, analytics, symbols, timeframes, strategies, lookback=lookback, risk_per_trade=risk_per_trade)
        
        await bybit_trading_system.start()

        # wss = 'wss://stream.bybit.com/v5/public/linear'
        
        # async with websockets.connect(wss) as ws:
        #     bybit_trading_system.subscribe_candle_stream(ws)

            # message_processing_task = asyncio.create_task(process_messages(ws, bybit_trading_system))
            # start_trading_system_task = asyncio.create_task(bybit_trading_system.start())

asyncio.run(main(), debug=True)