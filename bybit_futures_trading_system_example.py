import asyncio
from dotenv import load_dotenv
import os

from core.models.timeframe import Timeframe
from core.models.lookback import Lookback
from broker.futures_bybit_broker import FuturesBybitBroker
from datasource.bybit_datasource import BybitDataSource
from datasource.bybit_ws import BybitWSHandler
from backtest.backtest import Backtest
from executor.executor_factory import ExecutorFactory
from portfolio_management.portfolio_manager import PortfolioManager
from strategy_management.strategy_factory import StrategyActorFactory
from sync.csv_sync import CSVSync
from sync.log_sync import LogSync
from system.trend_system import TradingContext, TrendSystem

load_dotenv()

API_KEY = os.getenv('API_KEY')
API_SECRET = os.getenv('API_SECRET')
WSS = os.getenv('WSS')
IS_LIVE_MODE = os.getenv('LIVE_MODE') == "1"


async def main():
    lookback = Lookback.THREE_MONTH
    initial_account_size = 1000
    risk_per_trade = 0.0015
    risk_reward_ratio = 2.0
    slippage = 0.008
    leverage = 1
    timeframes = [
        Timeframe.ONE_MINUTE,
        Timeframe.FIVE_MINUTES,
        Timeframe.FIFTEEN_MINUTES
    ]

    strategies = [
        ['trend_follow', 'crossma', [50, 100, 14, 1.5]]
    ]

    LogSync()
    CSVSync()

    Backtest()

    broker = FuturesBybitBroker(API_KEY, API_SECRET)
    datasource = BybitDataSource(broker)
    ws_handler = BybitWSHandler(WSS)
    strategy_factory = StrategyActorFactory()
    executor_factory = ExecutorFactory(broker, slippage)

    portfolio = PortfolioManager(
        datasource,
        initial_account_size=initial_account_size,
        leverage=leverage,
        risk_reward_ratio=risk_reward_ratio,
        risk_per_trade=risk_per_trade
    )

    context = TradingContext(
        strategy_factory,
        executor_factory,
        datasource,
        ws_handler,
        broker,
        portfolio,
        timeframes,
        strategies,
        lookback,
        leverage,
        IS_LIVE_MODE
    )

    trading_system = TrendSystem(context)

    system_task = asyncio.create_task(trading_system.start())
    ws_handler_task = asyncio.create_task(ws_handler.run())

    try:
        await asyncio.gather(system_task, ws_handler_task)
    finally:
        system_task.cancel()
        ws_handler_task.cancel()

with asyncio.Runner() as runner:
    runner.run(main())
