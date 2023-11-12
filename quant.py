import asyncio
import logging
import os
import signal

import uvloop
from dotenv import load_dotenv

from backtest.backtest import Backtest
from broker.broker_factory import BrokerFactory
from core.models.lookback import Lookback
from core.models.timeframe import Timeframe
from datasource.bybit_ws import BybitWSHandler
from datasource.datasource_factory import DataSourceFactory
from exchange.exchange_factory import ExchangeFactory
from executor.order_executor_actor_factory import OrderExecutorActorFactory
from infrastructure.event_dispatcher.event_dispatcher import EventDispatcher
from infrastructure.event_store.event_store import EventStore
from infrastructure.logger import configure_logging
from infrastructure.shutdown import GracefulShutdown
from optimization.optimizer_factory import StrategyOptimizerFactory
from portfolio.portfolio import Portfolio
from position.position_actor_factory import PositionActorFactory
from position.position_factory import PositionFactory
from position.risk.break_even import PositionRiskBreakEvenStrategy
from position.size.fixed import PositionFixedSizeStrategy
from position.take_profit.risk_reward import PositionRiskRewardTakeProfitStrategy
from risk.risk_actor_factory import RiskActorFactory
from service.environment_secret_service import EnvironmentSecretService
from service.wasm_file_service import WasmFileService
from strategy.generator.strategy_generator_factory import StrategyGeneratorFactory
from strategy.signal_actor_factory import SignalActorFactory
from system.context import SystemContext
from system.squad_factory import SquadFactory
from system.system import System

asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())


load_dotenv()


BYBIT_WSS = os.getenv("BYBIT_WSS")
IS_LIVE_MODE = os.getenv("LIVE_MODE") == "1"
LOG_DIR = os.getenv("LOG_DIR")
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO").upper()
WASM_FOLDER = os.getenv("WASM_FOLDER")

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
    batch_size = 1597

    risk_per_trade = 0.0005
    risk_reward_ratio = 1.5
    risk_buffer = 0.0001
    break_even_percentage = 0.25
    leverage = 1
    initial_account_size = 1000
    lookback = Lookback.ONE_MONTH

    num_samples = 8
    active_strategy_num = 5
    max_generations = 1
    elite_count = 5
    mutation_rate = 0.05

    timeframes = [
        Timeframe.ONE_MINUTE,
    ]

    symbols_blacklist = [
        "USDCUSDT",
    ]

    event_store = EventStore(LOG_DIR, store_buf_size)
    event_bus = EventDispatcher(num_workers, multi_piority_group)

    Backtest(batch_size)
    Portfolio(initial_account_size, risk_per_trade)

    ws_handler = BybitWSHandler(BYBIT_WSS)

    datasource_factory = DataSourceFactory()
    broker_factory = BrokerFactory()
    exchange_factory = ExchangeFactory(EnvironmentSecretService())
    position_factory = PositionFactory(
        PositionFixedSizeStrategy(leverage, risk_per_trade),
        PositionRiskBreakEvenStrategy(break_even_percentage),
        PositionRiskRewardTakeProfitStrategy(risk_reward_ratio),
    )
    squad_factory = SquadFactory(
        SignalActorFactory(WasmFileService(WASM_FOLDER)),
        PositionActorFactory(initial_account_size, position_factory),
        RiskActorFactory(risk_buffer),
    )

    executor_factory = OrderExecutorActorFactory()

    strategy_optimization_factory = StrategyOptimizerFactory(
        max_generations, elite_count, mutation_rate
    )

    strategy_generator_factory = StrategyGeneratorFactory(
        num_samples, symbols_blacklist, timeframes
    )

    context = SystemContext(
        datasource_factory,
        broker_factory,
        exchange_factory,
        squad_factory,
        executor_factory,
        strategy_generator_factory,
        strategy_optimization_factory,
        lookback,
        active_strategy_num,
        leverage,
        IS_LIVE_MODE,
    )

    system = System(context)

    trader_task = asyncio.create_task(system.start())
    ws_handler_task = asyncio.create_task(ws_handler.run())
    shutdown_task = asyncio.create_task(graceful_shutdown.wait_for_exit_signal())

    try:
        logging.info("Started")
        await asyncio.gather(trader_task, ws_handler_task, shutdown_task)
    finally:
        logging.info("Closing...")

        shutdown_task.cancel()
        trader_task.cancel()
        ws_handler_task.cancel()
        system.stop()

        await event_bus.stop()
        await event_bus.wait()

        event_store.close()

        logging.info("Finished.")


with asyncio.Runner() as runner:
    runner.run(main())
