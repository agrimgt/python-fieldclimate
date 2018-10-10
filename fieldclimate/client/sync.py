import requests

from .base import BaseClient


class SynchronousClient(BaseClient):
    def request(self, method, route, data=None):
        url = self.full_url(route)
        h = self.get_headers(route, method)
        response = requests.request(method, url, headers=h)
        return response.json()
