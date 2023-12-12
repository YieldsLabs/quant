import asyncio
import logging
from enum import Enum, auto

from core.commands.account import UpdateAccountSize
from core.commands.broker import UpdateSettings
from core.events.backtest import BacktestEnded, BacktestStarted
from core.events.ohlcv import NewMarketDataReceived
from core.events.trade import TradeStarted
from core.interfaces.abstract_system import AbstractSystem
from core.models.broker import MarginMode, PositionMode
from core.models.exchange import ExchangeType
from core.models.lookback import Lookback
from core.models.optimizer import Optimizer
from core.models.order import OrderType
from core.models.strategy import Strategy
from core.models.symbol import Symbol
from core.models.timeframe import Timeframe
from core.models.ws import WSType
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
    TRADING_STOPPED = auto()
    SYSTEM_STOP = auto()


class System(AbstractSystem):
    def __init__(self, context: SystemContext):
        super().__init__()
        self.context = context
        self.state = SystemState.INIT

        self.event_queue = asyncio.Queue()
        self.active_strategy: list[tuple[Symbol, Timeframe, Strategy]] = []
        self.strategy: tuple[Symbol, Timeframe, Strategy] = []
        self.optimizer = None
        self.exchange = ExchangeType.BYBIT
        self.ws = WSType.BYBIT
        self.config = self.context.config_service.get("system")

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
            SystemState.TRADING: self._run_trading,
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

            await asyncio.gather(*[self._process_backtest(data) for data in batch])

            logger.info(f"Remaining time: {estimator.remaining_time():.2f}sec")

        await self.event_queue.put(Event.BACKTEST_COMPLETE)

    async def _run_optimization(self):
        logger.info("Run optimization")

        strategies = await self.query(
            GetTopStrategy(num=self.config["active_strategy_num"])
        )

        logger.info(
            [f"{strategy[0]}_{strategy[1]}{strategy[2]}" for strategy in strategies]
        )

        if not len(strategies):
            return await self.event_queue.put(Event.REGENERATE)

        if self.optimizer.done:
            return await self.event_queue.put(Event.OPTIMIZATION_COMPLETE)

        await self.optimizer.optimize()

        await self.event_queue.put(Event.RUN_BACKTEST)

    async def _run_verification(self):
        logger.info("Run verification")

        strategies = await self.query(
            GetTopStrategy(num=self.config["active_strategy_num"])
        )

        if not len(strategies):
            return await self.event_queue.put(Event.REGENERATE)

        async for batch in self._generate_batch(strategies):
            account_size = await self.query(GetBalance())
            await self.execute(UpdateAccountSize(account_size))

            await asyncio.gather(
                *[self._process_backtest(data, True) for data in batch]
            )

        await self.event_queue.put(Event.VERIFICATION_COMPLETE)

    async def _run_trading(self):
        logger.info("Run trading")

        strategies = await self.query(
            GetTopStrategy(num=self.config["active_strategy_num"])
        )

        if not len(strategies):
            return await self.event_queue.put(Event.REGENERATE)

        logger.info(
            [f"{strategy[0]}_{strategy[1]}{strategy[2]}" for strategy in strategies]
        )

        account_size = await self.query(GetBalance())
        await self.execute(UpdateAccountSize(account_size))

        await asyncio.gather(
            *[
                self.execute(
                    UpdateSettings(
                        symbol,
                        self.config["leverage"],
                        PositionMode.ONE_WAY,
                        MarginMode.ISOLATED,
                    )
                )
                for symbol, _, _ in strategies
            ]
        )

        await asyncio.gather(*[self._process_trading(data) for data in strategies])

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
        backtest_config = self.context.config_service.get("backtest")
        in_sample = Lookback.from_raw(backtest_config["in_sample"])
        out_sample = (
            None if verify else Lookback.from_raw(backtest_config["out_sample"])
        )

        datasource = self.context.datasource_factory.create(
            self.exchange,
            symbol,
            timeframe,
        )

        await self.dispatch(BacktestStarted(symbol, timeframe, strategy))

        actors = [
            self.context.signal_factory.create_actor(symbol, timeframe, strategy),
            self.context.position_factory.create_actor(symbol, timeframe, strategy),
            self.context.risk_factory.create_actor(symbol, timeframe, strategy),
            self.context.executor_factory.create_actor(
                OrderType.PAPER, symbol, timeframe, strategy
            ),
        ]

        logger.info(
            f"Backtest: strategy={symbol}_{timeframe}{strategy}, lookback={in_sample}"
        )

        iterator = datasource.fetch(
            in_sample,
            out_sample,
            backtest_config["batch_size"],
        )

        async for bar in iterator:
            await self.dispatch(
                NewMarketDataReceived(symbol, timeframe, bar.ohlcv, bar.closed)
            )

        last_bar = iterator.get_last_bar()

        if last_bar:
            await self.dispatch(
                BacktestEnded(symbol, timeframe, strategy, last_bar.ohlcv.close)
            )

        for actor in actors:
            actor.stop()

    async def _process_trading(
        self, data: tuple[Symbol, Timeframe, Strategy], verify=False
    ):
        symbol, timeframe, strategy = data

        logger.info(f"Prefetch data: {symbol}_{timeframe}{strategy}")

        signal_actor = self.context.signal_factory.create_actor(
            symbol, timeframe, strategy
        )

        datasource = self.context.datasource_factory.create(
            self.exchange,
            symbol,
            timeframe,
        )

        async for bar in datasource.fetch(
            Lookback.ONE_MONTH,
            None,
            self.context.config_service.get("backtest")["batch_size"],
        ):
            await self.dispatch(
                NewMarketDataReceived(symbol, timeframe, bar.ohlcv, bar.closed)
            )

        logger.info(f"Start trading: {symbol}_{timeframe}{strategy}")

        [
            signal_actor,
            self.context.position_factory.create_actor(symbol, timeframe, strategy),
            self.context.risk_factory.create_actor(symbol, timeframe, strategy),
            self.context.executor_factory.create_actor(
                OrderType.MARKET
                if self.context.config_service.get("system")["mode"] == 1
                else OrderType.PAPER,
                symbol,
                timeframe,
                strategy,
            ),
        ]

        await self.dispatch(TradeStarted(symbol, timeframe, strategy))

        ws_datasource = self.context.datasource_factory.create(
            self.ws,
            symbol,
            timeframe,
        )

        async for bar in ws_datasource.fetch():
            if bar:
                await self.dispatch(
                    NewMarketDataReceived(symbol, timeframe, bar.ohlcv, bar.closed)
                )

            if bar and bar.closed:
                logger.info(f"Tick: {symbol}_{timeframe}{strategy}:{bar}")
