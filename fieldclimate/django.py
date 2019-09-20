from django.conf import settings
from django.core.exceptions import ImproperlyConfigured

from fieldclimate import FieldClimateClient

err = (
    "Set your FieldClimate HMAC keys with FIELDCLIMATE_PUBLIC_KEY and "
    "FIELDCLIMATE_PRIVATE_KEY in your Django project's settings module."
)


class DjangoFieldClimateClient(FieldClimateClient):
    """Get HMAC keys from Django project's settings, or raise an error."""

    @classmethod
    def find_public_key(cls):
        try:
            return settings.FIELDCLIMATE_PUBLIC_KEY
        except AttributeError:
            raise ImproperlyConfigured(err)

    @classmethod
    def find_private_key(cls):
        try:
            return settings.FIELDCLIMATE_PRIVATE_KEY
        except AttributeError:
            raise ImproperlyConfigured(err)
