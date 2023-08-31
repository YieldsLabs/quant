import asyncio


class GracefulShutdown:
    def __init__(self):
        self.exit_event = asyncio.Event()

    async def wait_for_exit_signal(self):
        await self.exit_event.wait()

    def exit(self, _signal, _frame):
        print("Exiting...")
        self.exit_event.set()
