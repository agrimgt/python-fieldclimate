"""A client for the iMetos FieldClimate API."""
from fieldclimate.client import HmacClient, AsynchronousClient, SynchronousClient
from fieldclimate.commands import FieldClimateCommands

__all__ = ["FieldClimateAsync", "FieldClimateSync"]
__author__ = "Agrimanagement, Inc."


class FieldClimateAsync(FieldClimateCommands, HmacClient, AsynchronousClient):
    """Adapt aiohttp.ClientSession to FieldClimate's API.

    Full description of all methods: https://api.fieldclimate.com/v1/docs/

    To use this class, HMAC public and private keys must be provided either
    by specifying them in __init__ calls or subclass variables, or by, or by through
    (which must be provided to you by FieldClimate as described in the docs above)
    must be specified setting them in __init__ or in environment variables.

    To make requests, use FieldClimateClient as a context manager and await
    the api methods for dictionary responses:

    >>> async def print_user_json():
    ...     async with FieldClimateAsync() as client:
    ...         user = await client.get_user()
    ...         print(user)
    ...
    >>> import asyncio
    >>> asyncio.get_event_loop().run_until_complete(print_user_json())
    {'username': '...', }
    >>>

    TODO: Rate limiting not implemented currently. The server does not enforce any limit,
    but I have been able to DOS the server with too many requests. Use with caution!

    If you overload the server, it may start returning 502 response codes.
    """


class FieldClimateSync(FieldClimateCommands, HmacClient, SynchronousClient):
    """Adapt Requests to FieldClimate's API.

    Full description of all methods: https://api.fieldclimate.com/v1/docs/

    To use this class, HMAC public and private keys must be provided either
    by specifying them in __init__ calls or subclass variables, or by, or by through
    (which must be provided to you by FieldClimate as described in the docs above)
    must be specified setting them in __init__ or in environment variables.

    To make requests, call FieldClimateSync methods to get dictionary responses:

    >>> print(FieldClimateSync().get_user())
    {'username': '...', }
    >>>

    The interface is much easier compared to FieldClimateAsync, but it will
    perform much slower when you need to request a lot of stuff at once.
    """
