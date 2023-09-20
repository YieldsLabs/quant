import asyncio
import signal
from dotenv import load_dotenv
import os
import logging
import uvloop

from infrastructure.logger import configure_logging
from infrastructure.shutdown import GracefulShutdown
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
from system.genetic_system import GeneticSystem, TradingContext
from position.position_actor_factory import PositionActorFactory
from position.position_factory import PositionFactory
from risk.risk_actor_factory import RiskActorFactory
from portfolio.portfolio import Portfolio
from system.squad_factory import SquadFactory
from strategy.generator.trend_follow import TrendFollowStrategyGenerator


asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())


load_dotenv()


API_KEY = os.getenv('API_KEY')
API_SECRET = os.getenv('API_SECRET')
WSS = os.getenv('WSS')
IS_LIVE_MODE = os.getenv('LIVE_MODE') == "1"
LOG_DIR = os.getenv('LOG_DIR')
LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO').upper()


configure_logging(LOG_LEVEL)

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


graceful_shutdown = GracefulShutdown()
signal.signal(signal.SIGTERM, graceful_shutdown.exit)

async def main():
    logging.info('Initializing...')

    store_buf_size = 5000
    num_workers = os.cpu_count()
    multi_piority_group = 2

    lookback = Lookback.ONE_MONTH
    batch_size = 1597
    backtest_parallel = 2
    sample_size = 5
    max_generations = 10
    risk_per_trade = 0.005
    risk_reward_ratio = 2
    risk_buffer = 0.0001
    slippage = 0.0005
    leverage = 1
    initial_account_size = 1000

    timeframes = [
        Timeframe.FIVE_MINUTES,
        Timeframe.FIFTEEN_MINUTES,
    ]

    blacklist = [
        'USDCUSDT',
    ]
    
    trend_follow_wasm_path = './wasm/trend_follow.wasm'

    event_store = EventStore(LOG_DIR, store_buf_size)
    event_bus = EventDispatcher(num_workers, multi_piority_group)

    Backtest()
    Portfolio(initial_account_size, risk_per_trade)
    broker = FuturesBybitBroker(API_KEY, API_SECRET)
    datasource = BybitDataSource(broker)
    ws_handler = BybitWSHandler(WSS)

    trend_follow_strategy = TrendFollowStrategyGenerator()

    trend_follow_squad_factory = SquadFactory(
        SignalActorFactory(trend_follow_wasm_path),
        ExecutorActorFactory(slippage),
        PositionActorFactory(initial_account_size, PositionFactory(leverage, risk_per_trade, risk_reward_ratio)),
        RiskActorFactory(risk_buffer),
    )

    context = TradingContext(
        datasource,
        trend_follow_squad_factory,
        trend_follow_strategy,
        timeframes,
        blacklist,
        lookback,
        batch_size,
        backtest_parallel,
        sample_size,
        max_generations,
        leverage,
        IS_LIVE_MODE
    )

    trading_system = GeneticSystem(context)

    system_task = asyncio.create_task(trading_system.start())
    ws_handler_task = asyncio.create_task(ws_handler.run())
    shutdown_task = asyncio.create_task(graceful_shutdown.wait_for_exit_signal())

    try:
        logging.info('Started')
        await asyncio.gather(system_task, ws_handler_task, shutdown_task)
    finally:
        logging.info('Closing...')
        
        shutdown_task.cancel()
        system_task.cancel()
        ws_handler_task.cancel()

        trading_system.stop()
        
        await event_bus.stop()
        await event_bus.wait()

        event_store.close()

        logging.info('Finished.')

with asyncio.Runner() as runner:
    runner.run(main())
