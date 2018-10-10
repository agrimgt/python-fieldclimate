from Crypto.Hash import HMAC, SHA256
from datetime import datetime
from os import getenv


class HmacClient:
    public_key = None
    private_key = None
    env_prefix = "FIELDCLIMATE"

    def __init__(self, public_key=None, private_key=None, api_url=None):
        # resolve keys from init args, env vars, and class variables.
        self.public_key = public_key or self.env("PUBLIC_KEY") or self.public_key
        self.private_key = private_key or self.env("PRIVATE_KEY") or self.private_key
        assert (
            self.public_key and self.private_key
        ), "Public and private keys must be set for HMAC authentication to work."

    @classmethod
    def env(cls, VAR):
        return getenv(f"{cls.env_prefix}_{VAR}")

    def get_headers(self, route, method):
        headers = super(HmacClient, self).get_headers(route, method)
        # HMAC requires "Date" and "Authorization" headers.
        date = datetime.utcnow().strftime("%a, %d %b %Y %H:%M:%S GMT")
        message = method + route + date + self.public_key
        signature = HMAC.new(self.private_key.encode(), message.encode(), SHA256)
        headers.update(
            {
                "Date": date,
                "Authorization": f"hmac {self.public_key}:{signature.hexdigest()}",
            }
        )
        return headers
