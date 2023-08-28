import asyncio
from dotenv import load_dotenv
import os
from sync.log_sync import LogSync
import uvloop

from core.models.timeframe import Timeframe
from core.models.lookback import Lookback
from broker.futures_bybit_broker import FuturesBybitBroker
from datasource.bybit_datasource import BybitDataSource
from backtest.backtest import Backtest
from executor.executor_factory import ExecutorFactory
from strategy.signal_actor_factory import SignalActorFactory
from system.trend_system import TradingContext, TrendSystem

load_dotenv()

asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())

API_KEY = os.getenv('API_KEY')
API_SECRET = os.getenv('API_SECRET')
WSS = os.getenv('WSS')
IS_LIVE_MODE = os.getenv('LIVE_MODE') == "1"


async def main():
    lookback = Lookback.ONE_MONTH
    batch_size = 34
    initial_account_size = 1000
    risk_per_trade = 0.0015
    risk_reward_ratio = 2
    risk_buffer = 0.01
    slippage = 0.008
    leverage = 1
    timeframes = [
        # Timeframe.ONE_MINUTE,
        # Timeframe.FIVE_MINUTES,
        Timeframe.FIFTEEN_MINUTES
    ]

    strategies = [
        ['trend_follow', 'crossma', [50, 200, 14, 1.5]]
    ]

    LogSync()
    # CSVSync()

    Backtest()

    broker = FuturesBybitBroker(API_KEY, API_SECRET)
    datasource = BybitDataSource(broker)

    context = TradingContext(
        datasource,
        SignalActorFactory(),
        ExecutorFactory(slippage),
        timeframes,
        strategies,
        lookback,
        batch_size,
        leverage,
        IS_LIVE_MODE
    )

    trading_system = TrendSystem(context)

    system_task = asyncio.create_task(trading_system.start())
    # ws_handler_task = asyncio.create_task(ws_handler.run())

    try:
        await asyncio.gather(system_task)
    finally:
        system_task.cancel()
        # ws_handler_task.cancel()

with asyncio.Runner() as runner:
    runner.run(main())
