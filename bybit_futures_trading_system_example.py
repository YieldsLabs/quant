import asyncio
from dotenv import load_dotenv
import os

from core.timeframe import Timeframe
from broker.futures_bybit_broker import FuturesBybitBroker
from datasource.bybit_datasource import BybitDataSource
from datasource.bybit_ws import BybitWSHandler
from backtest.backtest import Backtest
from backtest.lookback import Lookback
from portfolio_management.portfolio_manager import PortfolioManager
from risk_management.risk_manager import RiskManager
from strategy_management.strategy_factory import StrategyActorFactory
from sync.csv_sync import CSVSync
from sync.log_sync import LogSync
from system.trading_system import TradingContext, TradingSystem

load_dotenv()

API_KEY = os.getenv('API_KEY')
API_SECRET = os.getenv('API_SECRET')
WSS = os.getenv('WSS')
IS_LIVE_MODE = os.getenv('LIVE_MODE') == "1"


async def main():
    lookback = Lookback.THREE_MONTH
    initial_account_size = 1000
    risk_per_trade = 0.0015
    risk_reward_ratio = 6.0
    leverage = 1
    timeframes = [
        Timeframe.ONE_MINUTE,
        Timeframe.FIVE_MINUTES,
        Timeframe.FIFTEEN_MINUTES
    ]

    LogSync()
    CSVSync()

    Backtest()
    RiskManager()

    broker = FuturesBybitBroker(API_KEY, API_SECRET)
    datasource = BybitDataSource(broker)
    ws_handler = BybitWSHandler(WSS)
    strategy_factory = StrategyActorFactory()
    portfolio = PortfolioManager(
        datasource,
        initial_account_size=initial_account_size,
        leverage=leverage,
        risk_reward_ratio=risk_reward_ratio,
        risk_per_trade=risk_per_trade
    )

    context = TradingContext(
        strategy_factory,
        datasource,
        ws_handler,
        broker,
        portfolio,
        timeframes,
        lookback,
        leverage,
        IS_LIVE_MODE
    )

    trading_system = TradingSystem(context)

    system_task = asyncio.create_task(trading_system.start())
    ws_handler_task = asyncio.create_task(ws_handler.run())

    try:
        await asyncio.gather(system_task, ws_handler_task)
    finally:
        system_task.cancel()
        ws_handler_task.cancel()

with asyncio.Runner() as runner:
    runner.run(main())
