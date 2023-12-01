import asyncio
import logging
import os
import signal

import uvloop
from dotenv import load_dotenv

from backtest.backtest import Backtest
from broker.broker_factory import BrokerFactory
from core.models.lookback import Lookback
from core.models.strategy import StrategyType
from core.models.timeframe import Timeframe
from datasource.bybit_ws import BybitWSHandler
from datasource.datasource_factory import DataSourceFactory
from exchange.exchange_factory import ExchangeFactory
from executor.order_executor_actor_factory import OrderExecutorActorFactory
from infrastructure.config import ConfigService
from infrastructure.event_dispatcher.event_dispatcher import EventDispatcher
from infrastructure.event_store.event_store import EventStore
from infrastructure.logger import configure_logging
from infrastructure.shutdown import GracefulShutdown
from optimization.optimizer_factory import StrategyOptimizerFactory
from portfolio.portfolio import Portfolio
from position.position_actor_factory import PositionActorFactory
from position.position_factory import PositionFactory
from position.risk.simple import PositionRiskSimpleStrategy
from position.size.optimal_f import PositionOptinalFSizeStrategy
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
    config = {
        "bus": {"num_workers": os.cpu_count(), "base_dir": LOG_DIR},
        "generator": {
            "timeframes": [str(Timeframe.ONE_MINUTE)],
            "blacklist": ["USDCUSDT"],
        },
        
    }

    config_service.update(config)

    event_store = EventStore(config_service)
    event_bus = EventDispatcher(config_service)

    exchange_factory = ExchangeFactory(EnvironmentSecretService())

    Backtest(DataSourceFactory(), exchange_factory, config_service)
    Portfolio(config_service)

    ws_handler = BybitWSHandler(BYBIT_WSS)
    broker_factory = BrokerFactory()

    position_factory = PositionFactory(
        PositionOptinalFSizeStrategy(),
        PositionRiskSimpleStrategy(),
        PositionRiskRewardTakeProfitStrategy(config_service),
    )

    squad_factory = SquadFactory(
        SignalActorFactory(WasmFileService(WASM_FOLDER)),
        PositionActorFactory(position_factory),
        RiskActorFactory(config_service),
    )

    executor_factory = OrderExecutorActorFactory()
    strategy_optimization_factory = StrategyOptimizerFactory(config_service)
    strategy_generator_factory = StrategyGeneratorFactory(config_service)

    trend_context = SystemContext(
        broker_factory,
        exchange_factory,
        squad_factory,
        executor_factory,
        strategy_generator_factory,
        strategy_optimization_factory,
        strategy_type=StrategyType.TREND,
        config=config_service,
    )

    trend_system = System(trend_context)

    trend_system_task = asyncio.create_task(trend_system.start())
    ws_handler_task = asyncio.create_task(ws_handler.run())
    shutdown_task = asyncio.create_task(graceful_shutdown.wait_for_exit_signal())

    try:
        logging.info("Started")
        await asyncio.gather(*[trend_system_task, ws_handler_task, shutdown_task])
    finally:
        logging.info("Closing...")
        shutdown_task.cancel()
        trend_system_task.cancel()
        ws_handler_task.cancel()

        await ws_handler.close()

        trend_system.stop()

        await event_bus.stop()
        await event_bus.wait()

        event_store.close()

        logging.info("Finished.")


with asyncio.Runner() as runner:
    runner.run(main())
