import asyncio
from dotenv import load_dotenv
import os
import uvloop

from core.models.timeframe import Timeframe
from core.models.lookback import Lookback
from broker.futures_bybit_broker import FuturesBybitBroker
from datasource.bybit_datasource import BybitDataSource
from datasource.bybit_ws import BybitWSHandler
from backtest.backtest import Backtest
from executor.executor_actor_factory import ExecutorActorFactory
from strategy.signal_actor_factory import SignalActorFactory
from system.trend_system import TradingContext, TrendSystem
from position.position_actor_factory import PositionActorFactory
from position.position_factory import PositionFactory
from risk.risk_actor_factory import RiskActorFactory
from portfolio.portfolio import Portfolio
from sync.log_sync import LogSync

load_dotenv()

asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())

API_KEY = os.getenv('API_KEY')
API_SECRET = os.getenv('API_SECRET')
WSS = os.getenv('WSS')
IS_LIVE_MODE = os.getenv('LIVE_MODE') == "1"


async def main():
    lookback = Lookback.ONE_MONTH
    batch_size = 144
    risk_per_trade = 0.0015
    risk_reward_ratio = 2
    risk_buffer = 0.01
    slippage = 0.008
    leverage = 1
    initial_account_size = 1000
    timeframes = [
        Timeframe.ONE_MINUTE,
        Timeframe.FIVE_MINUTES,
        Timeframe.FIFTEEN_MINUTES,
    ]
    symbols = ['SOLUSDT', 'APEUSDT', 'MATICUSDT']
    
    trend_follow_path = './wasm/trend_follow.wasm'
    trend_follow_strategies = [
        ['crossma', [50, 100, 14, 1.5]]
    ]

    LogSync()

    Backtest()
    Portfolio(initial_account_size, risk_per_trade)

    broker = FuturesBybitBroker(API_KEY, API_SECRET)
    datasource = BybitDataSource(broker)
    ws_handler = BybitWSHandler(WSS)

    context = TradingContext(
        datasource,
        SignalActorFactory(),
        ExecutorActorFactory(slippage),
        PositionActorFactory(
            initial_account_size,
            PositionFactory(leverage, risk_per_trade, risk_reward_ratio)
        ),
        RiskActorFactory(risk_buffer),
        timeframes,
        trend_follow_path,
        trend_follow_strategies,
        symbols,
        lookback,
        batch_size,
        leverage,
        IS_LIVE_MODE
    )

    trading_system = TrendSystem(context)

    system_task = asyncio.create_task(trading_system.start())
    ws_handler_task = asyncio.create_task(ws_handler.run())

    try:
        await asyncio.gather(system_task)
    finally:
        system_task.cancel()
        ws_handler_task.cancel()

with asyncio.Runner() as runner:
    runner.run(main())
