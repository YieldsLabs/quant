import asyncio
import logging
from collections import defaultdict
from enum import Enum, auto

from core.commands.broker import UpdateSettings
from core.event_decorators import event_handler
from core.events.system import DeployStrategy
from core.events.trade import TradeStarted
from core.interfaces.abstract_config import AbstractConfig
from core.interfaces.abstract_executor_actor_factory import AbstractExecutorActorFactory
from core.interfaces.abstract_feed_actor_factory import AbstractFeedActorFactory
from core.interfaces.abstract_position_actor_factory import AbstractPositionActorFactory
from core.interfaces.abstract_risk_actor_factory import AbstractRiskActorFactory
from core.interfaces.abstract_signal_actor_factory import AbstractSignalActorFactory
from core.interfaces.abstract_system import AbstractSystem
from core.models.broker import MarginMode, PositionMode
from core.models.exchange import ExchangeType
from core.models.feed import FeedType
from core.models.lookback import Lookback
from core.models.order_type import OrderType
from core.tasks.feed import StartHistoricalFeed, StartRealtimeFeed

logger = logging.getLogger(__name__)


class SystemState(Enum):
    IDLE = auto()
    PRETRADING = auto()
    TRADING = auto()
    STOPPED = auto()


class Event(Enum):
    CHANGE = auto()
    TRADING = auto()
    SYSTEM_STOP = auto()


class TradingSystem(AbstractSystem):
    def __init__(
        self,
        signal_factory: AbstractSignalActorFactory,
        position_factory: AbstractPositionActorFactory,
        risk_factory: AbstractRiskActorFactory,
        executor_factory: AbstractExecutorActorFactory,
        feed_factory: AbstractFeedActorFactory,
        config_service: AbstractConfig,
        exchange_type: ExchangeType,
    ):
        super().__init__()
        self.active_strategy = set()
        self.next_strategy = defaultdict(set)
        self.event_queue = asyncio.Queue()
        self.state = SystemState.IDLE
        self.config = config_service.get("system")
        self.signal_factory = signal_factory
        self.position_factory = position_factory
        self.risk_factory = risk_factory
        self.executor_factory = executor_factory
        self.feed_factory = feed_factory
        self.exchange_type = exchange_type

    @event_handler(DeployStrategy)
    async def _deploy_strategy(self, event: DeployStrategy):
        logger.info("Add a fresh strategy")

        logger.info(
            [f"{strategy[0]}_{strategy[1]}{strategy[2]}" for strategy in event.strategy]
        )

        for symbol, timeframe, strategy in event.strategy:
            self.next_strategy[(symbol, timeframe)].add((symbol, timeframe, strategy))

        await self.event_queue.put(Event.CHANGE)

    async def start(self):
        transitions = {
            SystemState.IDLE: {
                Event.CHANGE: SystemState.PRETRADING,
                Event.SYSTEM_STOP: SystemState.STOPPED,
            },
            SystemState.PRETRADING: {
                Event.TRADING: SystemState.TRADING,
                Event.SYSTEM_STOP: SystemState.STOPPED,
            },
            SystemState.TRADING: {
                Event.CHANGE: SystemState.PRETRADING,
                Event.SYSTEM_STOP: SystemState.STOPPED,
            },
        }

        while True:
            event = await self.event_queue.get()

            if self.state == SystemState.STOPPED:
                return

            self.state = transitions[self.state].get(event, self.state)
            await self._handle_state()

    def stop(self):
        self.event_queue.put_nowait(Event.SYSTEM_STOP)

    async def _handle_state(self):
        state_handlers = {
            SystemState.PRETRADING: self._run_pretrading,
            SystemState.TRADING: self._run_trading,
        }

        await state_handlers[self.state]()

    async def _run_pretrading(self):
        signal_actors = defaultdict(set)

        for _, strategies in self.next_strategy.items():
            for symbol, timeframe, strategy in strategies:
                await self.dispatch(TradeStarted(symbol, timeframe, strategy))

                signal_actor = self.signal_factory.create_actor(
                    symbol, timeframe, strategy
                )

                logger.info(f"Prefetch data: {symbol}_{timeframe}{strategy}")

                feed_actor = self.feed_factory.create_actor(
                    FeedType.HISTORICAL, symbol, timeframe, self.exchange_type
                )

                await self.run(
                    StartHistoricalFeed(symbol, timeframe, Lookback.ONE_MONTH, None)
                )

                feed_actor.stop()

                await self.wait()

                signal_actors[(symbol, timeframe)].add(signal_actor)

        for (symbol, timeframe), _ in self.next_strategy.items():
            await self.execute(
                UpdateSettings(
                    symbol,
                    min(symbol.max_leverage, self.config["leverage"]),
                    PositionMode.HEDGED,
                    MarginMode.CROSS,
                )
            )

            actors = (
                *signal_actors[(symbol, timeframe)],
                self.risk_factory.create_actor(symbol, timeframe),
                self.position_factory.create_actor(symbol, timeframe),
                self.executor_factory.create_actor(
                    OrderType.MARKET if self.config["mode"] == 1 else OrderType.PAPER,
                    symbol,
                    timeframe,
                ),
                self.feed_factory.create_actor(
                    FeedType.REALTIME,
                    symbol,
                    timeframe,
                    self.exchange_type,
                ),
            )

            self.active_strategy.add(actors)

        await self.event_queue.put(Event.TRADING)

    async def _run_trading(self):
        logger.info("Start trading")

        await asyncio.gather(
            *[
                self.run(StartRealtimeFeed(actor[0].symbol, actor[0].timeframe))
                for actor in self.active_strategy
            ]
        )
