"""Reusable clients for constructing sync/async API requests."""

__all__ = ["BaseClient", "HmacClient"]

import asyncio
from datetime import datetime
from os import getenv

import aiohttp
from Crypto.Hash import HMAC, SHA256


class BaseClient:
    """BaseClient wraps the aiohttp HTTP client library,
    providing both synchronous and asynchronous usage.

    Provides get(), post(), put(), and delete() methods.

    Conventions:
    - method: one of ["GET", "POST", "PUT", "DELETE"]
    - route: a url path that comes after base_url, starts with a slash.
    - data: optional payload for POST and PUT requests (can be a dict or None).

    """

    base_url = None
    aio_session = None

    def full_url(self, route):
        if self.base_url is None:
            raise TypeError("base_url must be set in order to derive full urls!")
        return self.base_url + route

    def get_headers(self, method, route):
        # tell server we always want json back.
        return {"Accept": "application/json"}

    async def __aenter__(self):
        if self.aio_session is None or self.aio_session.closed:
            self.aio_session = aiohttp.ClientSession()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self.aio_session is not None and not self.aio_session.closed:
            await self.aio_session.close()

    # provide a hint when used with the wrong with statement:
    def __enter__(self):
        raise TypeError("Use 'async with' instead of 'with'.")

    def __exit__(self, exc_type, exc_val, exc_tb):
        # __exit__ should exist in pair with __enter__ but never executed
        pass  # pragma: no cover

    async def _request_async(self, **request_args):
        # if self.aio_session is None or self.aio_session.closed:
        #     raise ValueError("Request called without open session.")
        async with self.aio_session.request(**request_args) as response:
            return await response.json()

    def request(self, method, route, data=None):
        """Use get_headers and full_url methods to construct a web request,
        returning a dictionary from the json data requested."""
        url = self.full_url(route)
        headers = self.get_headers(method, route)
        request_args = {"method": method, "url": url, "headers": headers, "data": data}

        # implementation of switching request method:
        if self.aio_session is not None and not self.aio_session.closed:
            # we are wrapped by an async context manager, so return an awaitable:
            return self._request_async(**request_args)
        else:
            # we are not asynchronous, so call our 'async with' code sequentially.
            loop = asyncio.get_event_loop()
            loop.run_until_complete(self.__aenter__())
            result = loop.run_until_complete(self._request_async(**request_args))
            loop.run_until_complete(self.__aexit__(None, None, None))
            return result

    # convenience wrappers around self.request():

    def get(self, route):
        return self.request("GET", route)

    def post(self, route, data=None):
        return self.request("POST", route, data=data)

    def put(self, route, data=None):
        return self.request("PUT", route, data=data)

    def delete(self, route):
        return self.request("DELETE", route)


class HmacClient(BaseClient):
    """Add HMAC authentication headers to all requests.

    Requires public and private HMAC keys to provide the "Date" and
    "Authorization" headers. These can be specified via:

    1. The public_key and private_key args in __init__,
    2. HMAC_PUBLIC_KEY and HMAC_PRIVATE_KEY environment variables.
    3. Subclassing HmacClient and setting them at the class level.

    Originally implemented as described in the FieldClimate docs:
    https://api.fieldclimate.com/v1/docs/#authentication-hmac

    """

    settings_prefix = "HMAC"
    public_key = None
    private_key = None

    def __init__(self, public_key=None, private_key=None, **kwargs):
        # set keys, preferring init args over env vars over class variables.
        self.public_key = public_key or self.find_setting("public_key")
        self.private_key = private_key or self.find_setting("private_key")
        super().__init__(**kwargs)

    @classmethod
    def find_setting(cls, var):
        VAR, var = var.upper(), var.lower()
        return getenv(f"{cls.settings_prefix}_{VAR}", getattr(cls, var, None))

    def get_headers(self, method, route):
        headers = super().get_headers(method, route)
        headers["Date"] = datetime.utcnow().strftime("%a, %d %b %Y %H:%M:%S GMT")
        if None in [self.public_key, self.private_key]:
            raise TypeError("HMAC headers require public_ and private_key settings.")
        message = method + route + headers["Date"] + self.public_key
        signature = HMAC.new(self.private_key.encode(), message.encode(), SHA256)
        headers["Authorization"] = f"hmac {self.public_key}:{signature.hexdigest()}"
        return headers
