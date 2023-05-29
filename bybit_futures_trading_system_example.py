import asyncio
from dotenv import load_dotenv
import os
from analytics.strategy_performance import StrategyPerformance
from broker.futures_bybit_broker import FuturesBybitBroker
from datasource.bybit_datasource import BybitDataSource
from datasource.bybit_ws import BybitWSHandler
from sync.csv_sync import CSVSync
from sync.log_sync import LogSync
from optimization.kmeans_inference import KMeansInference
from system.trading_system import TradingContext, TradingSystem

load_dotenv()

API_KEY = os.getenv('API_KEY')
API_SECRET = os.getenv('API_SECRET')
WSS = os.getenv('WSS')
IS_LIVE_MODE = os.getenv('LIVE_MODE') == "1"

backtest_lookback = 2016 * 4
risk_per_trade = 0.0015
leverage = 5


async def main():
    LogSync()
    CSVSync()

    broker = FuturesBybitBroker(API_KEY, API_SECRET)
    datasource = BybitDataSource(broker)
    ws_handler = BybitWSHandler(WSS)

    initial_account_size = await datasource.account_size()
    analytics = StrategyPerformance(initial_account_size, risk_per_trade)

    inference = KMeansInference(
        './optimization/model/kmeans_model.pkl',
        './optimization/model/scaler.pkl'
    )

    context = TradingContext(
        datasource,
        ws_handler,
        broker,
        analytics,
        inference,
        lookback=backtest_lookback,
        leverage=leverage,
        risk_per_trade=risk_per_trade,
        live_mode=IS_LIVE_MODE
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
