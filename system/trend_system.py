import asyncio
from enum import Enum, auto
from itertools import product
from random import shuffle

from core.commands.account import AccountUpdate
from core.commands.actor import SignalActorStart, SignalActorStop

from core.commands.backtest import BacktestRun
from core.commands.position import PositionCloseAll
from core.models.broker import MarginMode, PositionMode
from core.interfaces.abstract_system import AbstractSystem
from core.queries.position import PositionAll

from .trading_context import TradingContext


class SystemState(Enum):
    BACKTESTING = auto()
    OPTIMIZATION = auto()
    TRADING = auto()
    STOPPED = auto()


class TrendSystem(AbstractSystem):
    def __init__(self, context: TradingContext, state: SystemState = SystemState.BACKTESTING):
        super().__init__()
        self.context = context
        self.state = state

    async def start(self):
        while True:
            match self.state:
                case SystemState.BACKTESTING:
                    await self._run_backtest()
                    self.state = SystemState.OPTIMIZATION
                case SystemState.OPTIMIZATION:
                    await self._run_optimization()
                    self.state = SystemState.TRADING
                case SystemState.TRADING:
                    await self._run_trading()
                    self.state = SystemState.STOPPED
                case SystemState.STOPPED:
                    return

    async def _run_backtest(self):
        symbols = await self.context.datasource.symbols()

        symbols_and_timeframes = list(product(symbols, self.context.timeframes))
        
        shuffle(symbols_and_timeframes)

        strategies = [
            (symbol, timeframe, f'./signal/{strategy[0]}.wasm', strategy[1], strategy[2])
            for symbol, timeframe in symbols_and_timeframes
            for strategy in self.context.strategies
        ]

        async with self.context.executor_factory.create_executor(live=False):
            for symbol, timeframe, path, strategy_name, strategy_parameters in strategies:
                await self.dispatcher.execute(SignalActorStart(symbol, timeframe, path, strategy_name, strategy_parameters))

                amount = await self.context.datasource.account_size()

                await self.dispatcher.execute(AccountUpdate(amount))

                await self.dispatcher.execute(
                    BacktestRun(self.context.datasource, symbol, timeframe, self.context.lookback, self.context.batch_size))
                
        for symbol, timeframe in symbols_and_timeframes:
            await self.dispatcher.execute(SignalActorStop(symbol, timeframe))

    async def _run_optimization(self):
        await asyncio.sleep(0.1)

    async def _run_trading(self):
        print('Run trading')
        print(await self.dispatcher.query(PositionAll()))
        # top_strategies = await self.context.portfolio.get_top_strategies(3)

        # print(top_strategies)

        # if len(top_strategies) == 0:
        #     return

        # uniq_symbols = list(set([strategy.symbol for strategy in top_strategies]))

        # for symbol in uniq_symbols:
        #     self.context.broker.set_settings(symbol, self.context.leverage, position_mode=PositionMode.ONE_WAY, margin_mode=MarginMode.ISOLATED)

        # async with self.context.executor_factory.create_executor(self.context.live_mode):
        #     actors = list({
        #         actor
        #         for strategy in top_strategies
        #         for actor in self.strategy_actors
        #         if actor.strategy == strategy
        #     })

        #     for actor in actors:
        #         await self._ensure_actor_state(actor)

        #     symbols_and_timeframes = [(actor.strategy.symbol, actor.strategy.timeframe) for actor in actors]
            
        #     await self.context.ws_handler.subscribe(symbols_and_timeframes)

    async def _ensure_actor_state(self, actor):
        if await actor.running:
            await actor.stop()

        await actor.start()
