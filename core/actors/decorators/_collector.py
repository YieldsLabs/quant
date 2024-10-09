import asyncio
from functools import wraps
from typing import Any, AsyncIterable, Awaitable, Callable, Generator, Optional


def Producer(func: Callable[[Optional[Any]], Any]):
    @wraps(func)
    async def producer_wrapper(*args, **kwargs) -> AsyncIterable[Any]:
        result = func(*args, **kwargs)

        if isinstance(result, AsyncIterable):
            async for item in result:
                yield item
        else:

            def generator_wrapper() -> Generator[Any, None, None]:
                if not hasattr(result, "__iter__"):
                    raise TypeError(
                        f"Producer {func.__name__} did not return an iterable"
                    )
                yield from result

            for item in await asyncio.to_thread(generator_wrapper):
                yield item

    producer_wrapper._is_producer_ = True
    return producer_wrapper


def Consumer(func: Callable[[Any], Any]):
    if asyncio.iscoroutinefunction(func):

        @wraps(func)
        async def async_consumer_wrapper(*args, **kwargs) -> Awaitable[None]:
            return await func(*args, **kwargs)

        async_consumer_wrapper._is_consumer_ = True
        return async_consumer_wrapper
    else:

        @wraps(func)
        async def sync_consumer_wrapper(*args, **kwargs) -> Awaitable[None]:
            await asyncio.to_thread(func, *args, **kwargs)

        sync_consumer_wrapper._is_consumer_ = True
        return sync_consumer_wrapper
