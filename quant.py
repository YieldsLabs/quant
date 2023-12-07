import asyncio
import logging
import os
import signal

import uvloop
from dotenv import load_dotenv

from backtest import Backtest
from core.models.exchange import ExchangeType
from core.models.strategy import StrategyType
from datasource import DataSourceFactory
from exchange import ExchangeFactory, WSFactory
from executor import OrderExecutorActorFactory
from feed import Feed
from infrastructure.config import ConfigService
from infrastructure.event_dispatcher.event_dispatcher import EventDispatcher
from infrastructure.event_store.event_store import EventStore
from infrastructure.logger import configure_logging
from infrastructure.shutdown import GracefulShutdown
from optimization import StrategyOptimizerFactory
from portfolio import Portfolio
from position import PositionActorFactory, PositionFactory
from position.risk.simple import PositionRiskSimpleStrategy
from position.size.optimal_f import PositionOptinalFSizeStrategy
from position.take_profit.risk_reward import PositionRiskRewardTakeProfitStrategy
from risk import RiskActorFactory
from service import EnvironmentSecretService, SignalService, WasmFileService
from sor import SmartRouter
from strategy import SignalActorFactory
from strategy.generator import StrategyGeneratorFactory
from system.context import SystemContext
from system.system import System

asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())


load_dotenv()


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

    config_service = ConfigService()
    config_service.load(config_path="config.ini")
    config = {"bus": {"num_workers": os.cpu_count()}, "store": {"base_dir": LOG_DIR}}

    config_service.update(config)

    event_store = EventStore(config_service)
    event_bus = EventDispatcher(config_service)

    exchange_factory = ExchangeFactory(EnvironmentSecretService())
    ws_factory = WSFactory(EnvironmentSecretService())

    Portfolio(config_service)
    SmartRouter(exchange_factory, config_service)

    position_factory = PositionFactory(
        PositionOptinalFSizeStrategy(),
        PositionRiskSimpleStrategy(),
        PositionRiskRewardTakeProfitStrategy(config_service),
    )

    signal_actor_factory = SignalActorFactory(
        SignalService(WasmFileService(WASM_FOLDER))
    )
    position_actor_factory = PositionActorFactory(position_factory)
    risk_actor_factory = RiskActorFactory(config_service)
    executor_actor_factory = OrderExecutorActorFactory()
    datasource_factory = DataSourceFactory(exchange_factory, ws_factory)

    Backtest(
        signal_actor_factory,
        position_actor_factory,
        risk_actor_factory,
        executor_actor_factory,
        datasource_factory,
        config_service,
    )
    Feed(
        signal_actor_factory,
        position_actor_factory,
        risk_actor_factory,
        executor_actor_factory,
        datasource_factory,
        config_service,
    )

    trend_context = SystemContext(
        StrategyGeneratorFactory(config_service),
        StrategyOptimizerFactory(config_service),
        strategy_type=StrategyType.TREND,
        exchange_type=ExchangeType.BYBIT,
        config_service=config_service,
    )

    trend_system = System(trend_context)

    trend_system_task = asyncio.create_task(trend_system.start())
    shutdown_task = asyncio.create_task(graceful_shutdown.wait_for_exit_signal())

    try:
        logging.info("Started")
        await asyncio.gather(*[trend_system_task, shutdown_task])
    finally:
        logging.info("Closing...")
        shutdown_task.cancel()
        trend_system_task.cancel()

        trend_system.stop()

        await event_bus.stop()
        await event_bus.wait()

        event_store.close()

        logging.info("Finished.")


with asyncio.Runner() as runner:
    runner.run(main())
