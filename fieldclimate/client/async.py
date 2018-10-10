import aiohttp

from .base import BaseClient


class AsynchronousClient(BaseClient):
    session = None

    async def __aenter__(self):
        if self.session is None or self.session.closed:
            self.session = aiohttp.ClientSession()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self.session is not None and not self.session.closed:
            await self.session.close()

    # provide a hint when used with the wrong with statement
    def __enter__(self):
        raise SyntaxError("Use 'async with' instead of 'with'.")

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass  # pragma: no cover

    async def request(self, method, route, data=None):
        if self.session is None or self.session.closed:
            raise ValueError("Request called without open session.")
        url = self.full_url(route)
        h = self.get_headers(route, method)
        async with self.session.request(method, url, headers=h, data=data) as response:
            return await response.json()
