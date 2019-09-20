from django.conf import settings
from django.core.exceptions import ImproperlyConfigured

from fieldclimate import FieldClimateClient

err = (
    "Set your FieldClimate HMAC keys with FIELDCLIMATE_PUBLIC_KEY and "
    "FIELDCLIMATE_PRIVATE_KEY in your Django project's settings module."
)


class DjangoFieldClimateClient(FieldClimateClient):
    """Get HMAC keys from Django project's settings, or raise an error."""

    def __init__(self, **kwargs):
        # Deny usage of public_key and private_key kwargs.
        if "public_key" in kwargs or "private_key" in kwargs:
            client = self.__class__.__name__
            raise ImproperlyConfigured(
                f"{client} does not accept HMAC keys via init kwargs. {err}"
            )
        super(DjangoFieldClimateClient, self).__init__(**kwargs)

    @classmethod
    def find_public_key(cls):
        try:
            return settings.FIELDCLIMATE_PUBLIC_KEY
        except AttributeError:
            raise ImproperlyConfigured(f"Public key not found. {err}")

    @classmethod
    def find_private_key(cls):
        try:
            return settings.FIELDCLIMATE_PRIVATE_KEY
        except AttributeError:
            raise ImproperlyConfigured(f"Private key not found. {err}")
