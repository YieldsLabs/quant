import asyncio
import signal
from dotenv import load_dotenv
import os
import uvloop

from infrastructure.event_dispatcher.event_dispatcher import EventDispatcher
from infrastructure.event_store.event_store import EventStore
from core.models.timeframe import Timeframe
from core.models.lookback import Lookback
from broker.futures_bybit_broker import FuturesBybitBroker
from datasource.bybit_datasource import BybitDataSource
from datasource.bybit_ws import BybitWSHandler
from backtest.backtest import Backtest
from executor.executor_actor_factory import ExecutorActorFactory
from strategy.signal_actor_factory import SignalActorFactory
from system.trend_system import TradingContext, TrendSystem
from position.position_actor_factory import PositionActorFactory
from position.position_factory import PositionFactory
from risk.risk_actor_factory import RiskActorFactory
from portfolio.portfolio import Portfolio

load_dotenv()

asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())

API_KEY = os.getenv('API_KEY')
API_SECRET = os.getenv('API_SECRET')
WSS = os.getenv('WSS')
IS_LIVE_MODE = os.getenv('LIVE_MODE') == "1"
LOG_DIR = os.getenv('LOG_DIR')

class GracefulShutdown:
    def __init__(self):
        self.exit_event = asyncio.Event()

    async def wait_for_exit_signal(self):
        await self.exit_event.wait()

    def exit(self, _signal, _frame):
        print("Exiting...")
        self.exit_event.set()

graceful_shutdown = GracefulShutdown()

signal.signal(signal.SIGTERM, graceful_shutdown.exit)

async def main():
    lookback = Lookback.ONE_MONTH
    batch_size = 144
    risk_per_trade = 0.0015
    risk_reward_ratio = 2
    risk_buffer = 0.01
    slippage = 0.008
    leverage = 1
    initial_account_size = 1000
    timeframes = [
        Timeframe.ONE_MINUTE,
        Timeframe.FIVE_MINUTES,
        Timeframe.FIFTEEN_MINUTES,
    ]
    symbols = ['SOLUSDT', 'APEUSDT', 'MATICUSDT']
    
    trend_follow_path = './wasm/trend_follow.wasm'
    trend_follow_strategies = [
        ['crossma', [50, 100, 14, 1.5]]
    ]

    event_store = EventStore(LOG_DIR)
    event_bus = EventDispatcher(os.cpu_count(), 2)

    Backtest()
    Portfolio(initial_account_size, risk_per_trade)

    broker = FuturesBybitBroker(API_KEY, API_SECRET)
    datasource = BybitDataSource(broker)
    ws_handler = BybitWSHandler(WSS)

    context = TradingContext(
        datasource,
        SignalActorFactory(),
        ExecutorActorFactory(slippage),
        PositionActorFactory(
            initial_account_size,
            PositionFactory(leverage, risk_per_trade, risk_reward_ratio)
        ),
        RiskActorFactory(risk_buffer),
        timeframes,
        trend_follow_path,
        trend_follow_strategies,
        symbols,
        lookback,
        batch_size,
        leverage,
        IS_LIVE_MODE
    )

    trading_system = TrendSystem(context)

    system_task = asyncio.create_task(trading_system.start())
    ws_handler_task = asyncio.create_task(ws_handler.run())
    shutdown_task = asyncio.create_task(graceful_shutdown.wait_for_exit_signal())

    try:
        await asyncio.gather(system_task, ws_handler_task, shutdown_task)
    finally:
        shutdown_task.cancel()
        system_task.cancel()
        ws_handler_task.cancel()

        await event_bus.stop()
        await event_bus.wait()

        event_store.close()

with asyncio.Runner() as runner:
    runner.run(main())
