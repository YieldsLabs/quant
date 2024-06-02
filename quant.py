import asyncio
import logging
import os
import signal

import uvloop
from dotenv import load_dotenv

from copilot import CopilotActor
from core.models.exchange import ExchangeType
from exchange import ExchangeFactory, WSFactory
from executor import OrderExecutorActorFactory
from feed import FeedActorFactory
from infrastructure.config import ConfigService
from infrastructure.event_dispatcher.event_dispatcher import EventDispatcher
from infrastructure.logger import configure_logging
from infrastructure.shutdown import GracefulShutdown
from market import MarketActor
from optimization import StrategyOptimizerFactory
from portfolio import Portfolio
from position import PositionActorFactory, PositionFactory
from position.size.fixed import PositionFixedSizeStrategy
from risk import RiskActorFactory
from service import (
    EnvironmentSecretService,
    LLMService,
    SignalService,
    TimeSeriesService,
    WasmManager,
)
from sor import SmartRouter
from strategy import SignalActorFactory
from strategy.generator import StrategyGeneratorFactory
from system.backtest import BacktestSystem
from system.context import SystemContext
from system.trading import TradingSystem

asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())


load_dotenv()

REGIME = os.getenv("REGIME")
LOG_DIR = os.getenv("LOG_DIR")
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO").upper()
WASM_FOLDER = os.getenv("WASM_FOLDER")
COPILOT_MODEL_PATH = os.getenv("COPILOT_MODEL_PATH")

configure_logging(LOG_LEVEL)

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


graceful_shutdown = GracefulShutdown()
signal.signal(signal.SIGTERM, graceful_shutdown.exit)


async def main():
    logging.info("Initializing...")

    config_service = ConfigService()
    config_service.load(config_path=f"config.{REGIME}.ini")
    config = {
        "bus": {"num_workers": os.cpu_count() + 1},
        "store": {"base_dir": LOG_DIR},
        "copilot": {"model_path": COPILOT_MODEL_PATH},
    }

    config_service.update(config)

    event_bus = EventDispatcher(config_service)

    exchange_factory = ExchangeFactory(EnvironmentSecretService())
    ws_factory = WSFactory(EnvironmentSecretService())
    wasm = WasmManager(WASM_FOLDER)
    position_factory = PositionFactory(
        config_service,
        PositionFixedSizeStrategy(),
    )
    MarketActor(TimeSeriesService(wasm)).start()
    CopilotActor(LLMService(config_service)).start()
    Portfolio(config_service)
    SmartRouter(exchange_factory, config_service)

    signal_actor_factory = SignalActorFactory(SignalService(wasm))
    position_actor_factory = PositionActorFactory(position_factory, config_service)
    risk_actor_factory = RiskActorFactory(config_service)
    executor_actor_factory = OrderExecutorActorFactory()
    feed_actor_factory = FeedActorFactory(exchange_factory, ws_factory, config_service)

    trend_context = SystemContext(
        signal_actor_factory,
        position_actor_factory,
        risk_actor_factory,
        executor_actor_factory,
        feed_actor_factory,
        StrategyGeneratorFactory(config_service),
        StrategyOptimizerFactory(config_service),
        exchange_type=ExchangeType.BYBIT,
        config_service=config_service,
    )

    trend_system_a = BacktestSystem(trend_context)

    trading_system = TradingSystem(
        signal_actor_factory,
        position_actor_factory,
        risk_actor_factory,
        executor_actor_factory,
        feed_actor_factory,
        config_service,
        exchange_type=ExchangeType.BYBIT,
    )

    trend_system_a_task = asyncio.create_task(trend_system_a.start())
    trading_system_task = asyncio.create_task(trading_system.start())
    shutdown_task = asyncio.create_task(graceful_shutdown.wait_for_exit_signal())

    try:
        logging.info("Started")
        await asyncio.gather(*[trend_system_a_task, shutdown_task])
    finally:
        logging.info("Closing...")
        shutdown_task.cancel()
        trend_system_a_task.cancel()

        trading_system_task.cancel()

        trading_system.stop()

        await event_bus.stop()
        await event_bus.wait()

        logging.info("Finished.")


with asyncio.Runner(loop_factory=uvloop.new_event_loop) as runner:
    runner.run(main())
