import asyncio
import logging
from enum import Enum, auto

from core.commands.account import UpdateAccountSize
from core.commands.feed import StartHistoricalFeed
from core.events.backtest import BacktestEnded, BacktestStarted
from core.events.system import UpdatedStrategy
from core.interfaces.abstract_system import AbstractSystem
from core.models.feed import FeedType
from core.models.lookback import Lookback
from core.models.optimizer import Optimizer
from core.models.order import OrderType
from core.models.strategy import Strategy
from core.models.symbol import Symbol
from core.models.timeframe import Timeframe
from core.queries.account import GetBalance
from core.queries.broker import GetSymbols
from core.queries.portfolio import GetTopStrategy
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
        self.optimizer = None
        self.config = self.context.config_service.get("system")
        self.active_strategy = set()

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

        futures_symbols = await self.query(GetSymbols())

        generator = self.context.strategy_generator_factory.create(
            self.context.strategy_type, futures_symbols
        )
        self.optimizer = self.context.strategy_optimizer_factory.create(
            Optimizer.GENETIC,
            generator,
        )

        self.optimizer.init()

        await self.event_queue.put(Event.GENERATE_COMPLETE)

    async def _run_backtest(self):
        population = self.optimizer.population
        total_steps = len(population)

        logger.info(f"Run backtest for: {total_steps}")

        estimator = Estimator(total_steps // self.config["parallel_num"])

        async for batch in self._generate_batch(population):
            account_size = await self.query(GetBalance())
            await self.execute(UpdateAccountSize(account_size))

            await asyncio.gather(
                *[
                    self._process_backtest(data)
                    for data in batch
                    if data not in self.active_strategy
                ]
            )

            logger.info(f"Remaining time: {estimator.remaining_time():.2f}sec")

        await self.event_queue.put(Event.BACKTEST_COMPLETE)

    async def _run_optimization(self):
        logger.info("Run optimization")

        if self.optimizer.done:
            return await self.event_queue.put(Event.OPTIMIZATION_COMPLETE)

        strategies = await self.query(
            GetTopStrategy(num=self.config["active_strategy_num"])
        )

        if not len(strategies):
            return await self.event_queue.put(Event.REGENERATE)

        await self.optimizer.optimize()

        await self.event_queue.put(Event.RUN_BACKTEST)

    async def _run_verification(self):
        logger.info("Run verification")

        strategies = await self.query(
            GetTopStrategy(num=self.config["verify_strategy_num"])
        )

        if not len(strategies):
            return await self.event_queue.put(Event.REGENERATE)

        async for batch in self._generate_batch(strategies):
            account_size = await self.query(GetBalance())
            await self.execute(UpdateAccountSize(account_size))

            await asyncio.gather(
                *[
                    self._process_backtest(data, True)
                    for data in batch
                    if data not in self.active_strategy
                ]
            )

        await self.event_queue.put(Event.VERIFICATION_COMPLETE)

    async def _update_trading(self):
        logger.info("Deploy strategy for trading")
        strategies = await self.query(
            GetTopStrategy(num=self.config["active_strategy_num"])
        )

        self.active_strategy = set(strategies)

        await self.dispatch(UpdatedStrategy(type=self.context.strategy_type))
        await asyncio.sleep(self.config["reevaluate_timeout"])
        await self.event_queue.put(Event.REGENERATE)

    async def _generate_batch(self, data):
        batch = []

        for symbol, timeframe, strategy in data:
            batch.append((symbol, timeframe, strategy))

            if len(batch) == self.config["parallel_num"]:
                yield batch
                batch = []

        if batch:
            yield batch

    async def _process_backtest(
        self, data: tuple[Symbol, Timeframe, Strategy], verify=False
    ):
        symbol, timeframe, strategy = data

        await self.dispatch(BacktestStarted(symbol, timeframe, strategy))

        actors = [
            self.context.feed_factory.create_actor(
                FeedType.HISTORICAL,
                symbol,
                timeframe,
                strategy,
                self.context.exchange_type,
            ),
            self.context.signal_factory.create_actor(symbol, timeframe, strategy),
            self.context.position_factory.create_actor(symbol, timeframe, strategy),
            self.context.risk_factory.create_actor(symbol, timeframe, strategy),
            self.context.executor_factory.create_actor(
                OrderType.PAPER, symbol, timeframe, strategy
            ),
        ]

        backtest_config = self.context.config_service.get("backtest")
        in_sample = Lookback.from_raw(backtest_config["in_sample"])
        out_sample = (
            None if verify else Lookback.from_raw(backtest_config["out_sample"])
        )

        logger.info(
            f"Backtest: strategy={symbol}_{timeframe}{strategy}, lookback={in_sample}"
        )

        await self.execute(
            StartHistoricalFeed(symbol, timeframe, in_sample, out_sample)
        )

        if actors[0].last_bar:
            await self.dispatch(
                BacktestEnded(
                    symbol, timeframe, strategy, actors[0].last_bar.ohlcv.close
                )
            )

        for actor in actors:
            actor.stop()
