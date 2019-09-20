import asyncio
from functools import partial

import curio
import trio


def async_test(coro):
    def wrapper(*args, **kwargs):
        return asyncio.new_event_loop().run_until_complete(coro(*args, **kwargs))

    return wrapper


def curio_test(coro):
    def wrapper(*args, **kwargs):
        return curio.run(coro(*args, **kwargs))

    return wrapper


def trio_test(coro):
    # trio_test already exists in the trio.testing module,
    # ... but I could not get it to work :(
    def wrapper(*args, **kwargs):
        return trio.run(partial(coro, *args, **kwargs))

    return wrapper
