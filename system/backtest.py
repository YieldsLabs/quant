import asyncio
import logging
from enum import Enum, auto

from core.commands.factor import EnvolveGeneration, InitGeneration
from core.commands.portfolio import PortfolioReset
from core.events.backtest import BacktestEnded, BacktestStarted
from core.events.system import DeployStrategy
from core.interfaces.abstract_system import AbstractSystem
from core.models.cap import CapType
from core.models.feed import FeedType
from core.models.lookback import Lookback
from core.models.order_type import OrderType
from core.models.strategy import Strategy
from core.models.symbol import Symbol
from core.models.timeframe import Timeframe
from core.queries.factor import GetGeneration
from core.queries.portfolio import GetPortfolioRank
from core.tasks.feed import StartHistoricalFeed
from infrastructure.estimator import Estimator

from .context import SystemContext

logger = logging.getLogger(__name__)


class SystemState(Enum):
    INIT = auto()
    GENERATE = auto()
    BACKTEST = auto()
    OPTIMIZATION = auto()
    VERIFICATION = auto()
    TRADING = auto()
    STOPPED = auto()


class Event(Enum):
    GENERATE_COMPLETE = auto()
    RUN_BACKTEST = auto()
    REGENERATE = auto()
    BACKTEST_COMPLETE = auto()
    OPTIMIZATION_COMPLETE = auto()
    VERIFICATION_COMPLETE = auto()
    SYSTEM_STOP = auto()


class BacktestSystem(AbstractSystem):
    def __init__(self, context: SystemContext):
        super().__init__()
        self.context = context
        self.state = SystemState.INIT
        self.event_queue = asyncio.Queue()
        self.active_strategy = set()
        self.default_cap = CapType.A

    async def start(self):
        transitions = {
            SystemState.INIT: {
                Event.REGENERATE: SystemState.GENERATE,
                Event.SYSTEM_STOP: SystemState.STOPPED,
            },
            SystemState.GENERATE: {
                Event.GENERATE_COMPLETE: SystemState.BACKTEST,
                Event.SYSTEM_STOP: SystemState.STOPPED,
            },
            SystemState.BACKTEST: {
                Event.BACKTEST_COMPLETE: SystemState.OPTIMIZATION,
                Event.SYSTEM_STOP: SystemState.STOPPED,
            },
            SystemState.OPTIMIZATION: {
                Event.OPTIMIZATION_COMPLETE: SystemState.VERIFICATION,
                Event.REGENERATE: SystemState.GENERATE,
                Event.RUN_BACKTEST: SystemState.BACKTEST,
                Event.SYSTEM_STOP: SystemState.STOPPED,
            },
            SystemState.VERIFICATION: {
                Event.VERIFICATION_COMPLETE: SystemState.TRADING,
                Event.REGENERATE: SystemState.GENERATE,
                Event.SYSTEM_STOP: SystemState.STOPPED,
            },
            SystemState.TRADING: {
                Event.REGENERATE: SystemState.GENERATE,
                Event.SYSTEM_STOP: SystemState.STOPPED,
            },
        }

        await self.event_queue.put(Event.REGENERATE)

        while True:
            event = await self.event_queue.get()

            if self.state == SystemState.STOPPED:
                return

            self.state = transitions[self.state].get(event, self.state)
            await self._handle_state()

    async def _handle_state(self):
        state_handlers = {
            SystemState.GENERATE: self._generate,
            SystemState.BACKTEST: self._run_backtest,
            SystemState.OPTIMIZATION: self._run_optimization,
            SystemState.VERIFICATION: self._run_verification,
            SystemState.TRADING: self._update_trading,
        }

        await state_handlers[self.state]()

    def stop(self):
        self.event_queue.put_nowait(Event.SYSTEM_STOP)

    async def _generate(self):
        logger.info("Generate a new population")

        await self.execute(InitGeneration(self.context.datasource, self.default_cap))

        await self.event_queue.put(Event.GENERATE_COMPLETE)

    async def _run_backtest(self):
        population, generation = await self.query(GetGeneration())

        total_steps = len(population)
        logger.info(f"Run backtest for: {total_steps}, generation: {generation + 1}")

        estimator = Estimator(total_steps)

        for strategy in population:
            await self._process_backtest(strategy)

            logger.info(f"Remaining backtest time: {estimator.remaining_time()}")

        await self.event_queue.put(Event.BACKTEST_COMPLETE)

    async def _run_optimization(self):
        logger.info("Run optimization")

        await self.execute(EnvolveGeneration(self.context.datasource, self.default_cap))

        await self.event_queue.put(Event.RUN_BACKTEST)

    async def _run_verification(self):
        logger.info("Run verification")

        population, _ = await self.query(GetGeneration())

        if not len(population):
            return await self.event_queue.put(Event.REGENERATE)

        await self.execute(PortfolioReset())

        all_strategy = set(population)

        for data in all_strategy:
            await self._process_backtest(data, True)

        await self.event_queue.put(Event.VERIFICATION_COMPLETE)

    async def _update_trading(self):
        logger.info("Deploy strategy for trading")

        population, _ = await self.query(GetGeneration())

        if not len(population):
            return await self.event_queue.put(Event.REGENERATE)

        await self.dispatch(DeployStrategy(strategy=population))

    async def _process_backtest(
        self, data: tuple[Symbol, Timeframe, Strategy], verify=False
    ):
        symbol, timeframe, strategy = data

        await self.dispatch(BacktestStarted(symbol, timeframe, strategy))

        actors = [
            self.context.signal_factory.create_actor(symbol, timeframe, strategy),
            self.context.position_factory.create_actor(symbol, timeframe),
            self.context.risk_factory.create_actor(symbol, timeframe),
            self.context.executor_factory.create_actor(
                OrderType.PAPER, symbol, timeframe
            ),
            self.context.feed_factory.create_actor(
                FeedType.HISTORICAL,
                symbol,
                timeframe,
                self.context.datasource,
            ),
        ]

        _, generation = await self.query(GetGeneration())

        max_gen = self.context.config_service.get("factor").get("max_generations")
        window_size = self.context.config_service.get("backtest").get("window_size")

        verify_sample = 2
        in_sample = window_size
        out_sample = max((max_gen - generation) * window_size - in_sample, 0)

        in_lookback = Lookback.from_raw(verify_sample if verify else in_sample)
        out_lookback = None if verify else Lookback.from_raw(out_sample + verify_sample)

        logger.info(
            f"Backtest: generation={generation}, strategy={symbol}_{timeframe}{strategy}, in_lookback={in_lookback}, out_lookback={out_lookback}"
        )

        await self.run(
            StartHistoricalFeed(
                symbol, timeframe, self.context.datasource, in_lookback, out_lookback
            )
        )

        await self.dispatch(BacktestEnded(symbol, timeframe, strategy))

        for actor in actors:
            actor.stop()
