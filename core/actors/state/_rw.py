import asyncio


class RWLock:
    def __init__(self):
        self._readers = 0
        self._writer = False
        self._waiting_writers: int = 0
        self._lock = asyncio.Lock()
        self._readers_ok = asyncio.Condition(self._lock)
        self._writers_ok = asyncio.Condition(self._lock)

    async def acquire_reader(self):
        async with self._lock:
            while self._writer or self._waiting_writers > 0:
                await self._readers_ok.wait()

            self._readers += 1

    async def release_reader(self):
        async with self._lock:
            self._readers -= 1

            if self._readers == 0:
                self._writers_ok.notify()

    async def acquire_writer(self):
        async with self._lock:
            self._waiting_writers += 1

            try:
                while self._writer or self._readers > 0:
                    await self._writers_ok.wait()

                self._writer = True
            finally:
                self._waiting_writers -= 1

    async def release_writer(self):
        async with self._lock:
            self._writer = False

            self._readers_ok.notify_all()
            self._writers_ok.notify()
