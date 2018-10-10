class BaseClient:
    """BaseClient provides get(), post(), put(), and delete() methods.

    Subclasses must provide the implementation for request().

    Conventions:
    - method: one of ["GET", "POST", "PUT", "DELETE"]
    - route: a url path that comes after base_url.
    - data: optional payload for POST and PUT requests (can be a dict or None).
    """

    base_url = None

    def __init__(self, base_url=None):
        self.base_url = base_url or self.base_url
        assert self.base_url is not None, "base_url must be set!"

    def full_url(self, route):
        return self.base_url + route

    def get_headers(self, method, route):
        return {"Accept": "application/json"}

    def request(self, method, route, data=None):
        """Use get_headers and full_url methods to construct a web request,
        returning a dictionary from the json data requested."""
        raise NotImplementedError

    def get(self, route):
        return self.request("GET", route)

    def post(self, route, data):
        return self.request("POST", route, data=data)

    def put(self, route, data):
        return self.request("PUT", route, data=data)

    def delete(self, route):
        return self.request("DELETE", route)
