import asyncio
import logging
import os
import signal

import uvloop
from dotenv import load_dotenv

from backtest.backtest import Backtest
from broker.futures_bybit_broker import FuturesBybitBroker
from core.models.lookback import Lookback
from core.models.timeframe import Timeframe
from datasource.bybit_datasource import BybitDataSource
from datasource.bybit_ws import BybitWSHandler
from executor.executor_actor_factory import ExecutorActorFactory
from infrastructure.event_dispatcher.event_dispatcher import EventDispatcher
from infrastructure.event_store.event_store import EventStore
from infrastructure.logger import configure_logging
from infrastructure.shutdown import GracefulShutdown
from portfolio.portfolio import Portfolio
from position.position_actor_factory import PositionActorFactory
from position.position_factory import PositionFactory
from position.risk.break_even import PositionRiskBreakEvenStrategy
from position.size.fixed import PositionFixedSizeStrategy
from position.take_profit.risk_reward import PositionRiskRewardTakeProfitStrategy
from risk.risk_actor_factory import RiskActorFactory
from strategy.generator.trend_follow import TrendFollowStrategyGenerator
from strategy.signal_actor_factory import SignalActorFactory
from system.genetic_system import GeneticSystem, TradingContext
from system.squad_factory import SquadFactory

asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())


load_dotenv()


API_KEY = os.getenv("API_KEY")
API_SECRET = os.getenv("API_SECRET")
WSS = os.getenv("WSS")
IS_LIVE_MODE = os.getenv("LIVE_MODE") == "1"
LOG_DIR = os.getenv("LOG_DIR")
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO").upper()


configure_logging(LOG_LEVEL)

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


graceful_shutdown = GracefulShutdown()
signal.signal(signal.SIGTERM, graceful_shutdown.exit)


async def main():
    logging.info("Initializing...")

    store_buf_size = 5000
    num_workers = os.cpu_count()
    multi_piority_group = 2

    lookback = Lookback.ONE_MONTH
    batch_size = 1597
    backtest_parallel = 2
    sample_size = 13
    max_generations = 3
    risk_per_trade = 0.005
    risk_reward_ratio = 2
    risk_buffer = 0.0001
    slippage = 0.0005
    break_even_percentage = 0.25
    leverage = 1
    initial_account_size = 1000
    elite_count = 3
    mutation_rate = 0.05

    timeframes = [
        Timeframe.ONE_MINUTE,
        Timeframe.FIVE_MINUTES,
        Timeframe.FIFTEEN_MINUTES,
    ]

    blacklist = [
        "USDCUSDT",
    ]

    trend_follow_wasm_path = "./wasm/trend_follow.wasm"

    event_store = EventStore(LOG_DIR, store_buf_size)
    event_bus = EventDispatcher(num_workers, multi_piority_group)

    Backtest()
    Portfolio(initial_account_size, risk_per_trade)
    broker = FuturesBybitBroker(API_KEY, API_SECRET)
    datasource = BybitDataSource(broker)
    ws_handler = BybitWSHandler(WSS)

    strategy_generator = TrendFollowStrategyGenerator()

    fixed_size_strategy = PositionFixedSizeStrategy(leverage, risk_per_trade)
    break_even_risk = PositionRiskBreakEvenStrategy(break_even_percentage)
    take_profit_strategy = PositionRiskRewardTakeProfitStrategy(risk_reward_ratio)
    position_factory = PositionFactory(
        fixed_size_strategy, break_even_risk, take_profit_strategy
    )

    trend_follow_squad_factory = SquadFactory(
        SignalActorFactory(trend_follow_wasm_path),
        ExecutorActorFactory(slippage),
        PositionActorFactory(initial_account_size, position_factory),
        RiskActorFactory(risk_buffer),
    )

    context = TradingContext(
        datasource,
        trend_follow_squad_factory,
        strategy_generator,
        timeframes,
        blacklist,
        lookback,
        batch_size,
        backtest_parallel,
        sample_size,
        max_generations,
        leverage,
        IS_LIVE_MODE,
    )

    trading_system = GeneticSystem(context, elite_count, mutation_rate)

    system_task = asyncio.create_task(trading_system.start())
    ws_handler_task = asyncio.create_task(ws_handler.run())
    shutdown_task = asyncio.create_task(graceful_shutdown.wait_for_exit_signal())

    try:
        logging.info("Started")
        await asyncio.gather(system_task, ws_handler_task, shutdown_task)
    finally:
        logging.info("Closing...")

        shutdown_task.cancel()
        system_task.cancel()
        ws_handler_task.cancel()

        trading_system.stop()

        await event_bus.stop()
        await event_bus.wait()

        event_store.close()

        logging.info("Finished.")


with asyncio.Runner() as runner:
    runner.run(main())
